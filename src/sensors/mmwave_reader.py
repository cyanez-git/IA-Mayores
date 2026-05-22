"""
Lector de sensores mmWave Zigbee (ZY-M100-1) vía Zigbee2MQTT.

Z2M publica un topic por sensor: zigbee2mqtt/<friendly_name>
con un JSON tipo:
  {
    "presence": true,
    "target_distance": 145,         # cm
    "motion_state": "small",        # 'none' | 'small' | 'large'
    "radar_sensitivity": 7,
    "linkquality": 200
  }

MOCK_MODE=true genera datos simulados para desarrollo sin hardware.
"""
import json
import os
import random
import threading
import time
from dataclasses import dataclass

import paho.mqtt.client as mqtt

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
Z2M_TOPIC_WILDCARD = "zigbee2mqtt/+"   # se suscribe a todos los sensores Z2M
LEGACY_TOPIC      = "samp/mmwave"       # retrocompat: dispositivos que publican directo
MOCK_INTERVAL = 3
SENSOR_NAME_PREFIX = "mmwave"           # solo trackeamos friendly_names que arranquen con esto


@dataclass
class MmWaveReading:
    presence_detected: bool
    fall_detected: bool
    distance_cm: float
    movement_speed: float
    timestamp: float
    source: str = "unknown"   # nombre del sensor que generó la lectura


_per_sensor: dict[str, MmWaveReading] = {}
_lock = threading.Lock()


def get_latest() -> MmWaveReading | None:
    """Lectura agregada: presencia si CUALQUIER sensor detecta, distancia mínima."""
    with _lock:
        if not _per_sensor:
            return None
        readings = list(_per_sensor.values())
        any_presence = any(r.presence_detected for r in readings)
        any_fall     = any(r.fall_detected for r in readings)
        active = [r for r in readings if r.presence_detected]
        distance = min((r.distance_cm for r in active), default=0.0)
        speed    = max((r.movement_speed for r in active), default=0.0)
        sources  = ",".join(r.source for r in active) or "none"
        return MmWaveReading(
            presence_detected=any_presence,
            fall_detected=any_fall,
            distance_cm=distance,
            movement_speed=speed,
            timestamp=time.time(),
            source=sources,
        )


def get_per_sensor() -> dict[str, MmWaveReading]:
    """Lecturas individuales para mostrar en el dashboard."""
    with _lock:
        return dict(_per_sensor)


def _set_reading(name: str, reading: MmWaveReading):
    with _lock:
        _per_sensor[name] = reading


def _parse_z2m_payload(name: str, data: dict) -> MmWaveReading | None:
    """Convierte el JSON de Z2M (ZY-M100-1) al formato interno."""
    if "presence" not in data and "target_distance" not in data:
        return None  # mensaje no relevante (ej: bridge info, availability)

    presence = bool(data.get("presence", False))
    distance_cm = float(data.get("target_distance", 0))
    motion = str(data.get("motion_state", "none")).lower()
    speed_map = {"none": 0.0, "small": 0.3, "large": 1.2}
    movement_speed = speed_map.get(motion, 0.0)

    return MmWaveReading(
        presence_detected=presence,
        fall_detected=False,   # ZY-M100 no detecta caídas — fusion lo decide
        distance_cm=distance_cm,
        movement_speed=movement_speed,
        timestamp=time.time(),
        source=name,
    )


def _mock_loop():
    """Genera lecturas simuladas para dos sensores en paralelo."""
    sensors = ["mmwave_living", "mmwave_dormitorio"]
    while True:
        for s in sensors:
            scenario = random.choices(
                ["present_normal", "absent"], weights=[70, 30]
            )[0]
            if scenario == "present_normal":
                reading = MmWaveReading(
                    presence_detected=True,
                    fall_detected=False,
                    distance_cm=round(random.uniform(80, 300), 1),
                    movement_speed=round(random.uniform(0.0, 0.5), 2),
                    timestamp=time.time(),
                    source=s,
                )
            else:
                reading = MmWaveReading(
                    presence_detected=False,
                    fall_detected=False,
                    distance_cm=0.0,
                    movement_speed=0.0,
                    timestamp=time.time(),
                    source=s,
                )
            _set_reading(s, reading)
        time.sleep(MOCK_INTERVAL)


def _real_mqtt_loop():
    def on_message(client, userdata, msg):
        topic = msg.topic
        try:
            data = json.loads(msg.payload)
        except Exception:
            return

        if topic == LEGACY_TOPIC:
            try:
                reading = MmWaveReading(**data)
                _set_reading(reading.source or "legacy", reading)
            except Exception as e:
                print(f"[mmWave] Error en topic legacy: {e}")
            return

        # zigbee2mqtt/<friendly_name>
        if topic.startswith("zigbee2mqtt/"):
            name = topic.split("/", 1)[1]
            if not name.startswith(SENSOR_NAME_PREFIX):
                return  # ignorar otros dispositivos Zigbee no relacionados
            reading = _parse_z2m_payload(name, data)
            if reading:
                _set_reading(name, reading)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.subscribe([(Z2M_TOPIC_WILDCARD, 0), (LEGACY_TOPIC, 0)])
    print(f"[mmWave] Suscrito a {Z2M_TOPIC_WILDCARD} y {LEGACY_TOPIC}")
    client.loop_forever()


def start(background: bool = True):
    target = _mock_loop if MOCK_MODE else _real_mqtt_loop
    mode = "MOCK" if MOCK_MODE else "Zigbee2MQTT"
    print(f"[mmWave] Iniciando en modo {mode}")
    t = threading.Thread(target=target, daemon=True)
    t.start()
    if not background:
        t.join()
