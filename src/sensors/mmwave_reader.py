"""
Lector de sensor mmWave (HiLink LD2410C o Seeed MR60BHA1 vía WiFi/MQTT).
MOCK_MODE=true genera datos simulados.
"""
import json
import os
import random
import threading
import time
from dataclasses import dataclass, asdict

import paho.mqtt.client as mqtt

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC_IN = "samp/mmwave"    # el sensor publica acá
MOCK_INTERVAL = 3                # segundos entre lecturas mock


@dataclass
class MmWaveReading:
    presence_detected: bool
    fall_detected: bool
    distance_cm: float     # distancia al objeto más cercano
    movement_speed: float  # velocidad de movimiento (m/s)
    timestamp: float


_latest: MmWaveReading | None = None
_lock = threading.Lock()


def get_latest() -> MmWaveReading | None:
    with _lock:
        return _latest


def _set_latest(reading: MmWaveReading):
    global _latest
    with _lock:
        _latest = reading


def _mock_loop():
    """Genera lecturas simuladas en un thread."""
    while True:
        scenario = random.choices(
            ["present_normal", "present_fall", "absent"],
            weights=[75, 5, 20]
        )[0]

        if scenario == "present_normal":
            reading = MmWaveReading(
                presence_detected=True,
                fall_detected=False,
                distance_cm=round(random.uniform(80, 300), 1),
                movement_speed=round(random.uniform(0.0, 0.5), 2),
                timestamp=time.time(),
            )
        elif scenario == "present_fall":
            reading = MmWaveReading(
                presence_detected=True,
                fall_detected=True,
                distance_cm=round(random.uniform(20, 80), 1),
                movement_speed=round(random.uniform(1.5, 4.0), 2),
                timestamp=time.time(),
            )
        else:
            reading = MmWaveReading(
                presence_detected=False,
                fall_detected=False,
                distance_cm=0.0,
                movement_speed=0.0,
                timestamp=time.time(),
            )

        _set_latest(reading)
        time.sleep(MOCK_INTERVAL)


def _real_mqtt_loop():
    """Suscribe al topic MQTT del sensor mmWave real."""
    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            reading = MmWaveReading(**data)
            _set_latest(reading)
        except Exception as e:
            print(f"[mmWave] Error parseando mensaje: {e}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.subscribe(MQTT_TOPIC_IN)
    print(f"[mmWave] Suscrito a {MQTT_TOPIC_IN}")
    client.loop_forever()


def start(background: bool = True):
    """Inicia el reader en un thread de fondo."""
    target = _mock_loop if MOCK_MODE else _real_mqtt_loop
    mode = "MOCK" if MOCK_MODE else f"MQTT {MQTT_TOPIC_IN}"
    print(f"[mmWave] Iniciando en modo {mode}")
    t = threading.Thread(target=target, daemon=True)
    t.start()
    if not background:
        t.join()
