"""
BLE reader para wearable (Mi Band 8 o similar).
MOCK_MODE=true genera datos simulados sin hardware.
"""
import asyncio
import json
import os
import random
import time
from dataclasses import dataclass, asdict

import paho.mqtt.client as mqtt

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = "samp/wearable"
WEARABLE_MAC = os.getenv("WEARABLE_MAC", "")  # MAC del wearable real


@dataclass
class WearableReading:
    heart_rate: int        # bpm
    accel_x: float         # g
    accel_y: float
    accel_z: float
    impact_detected: bool
    timestamp: float


def _mock_reading() -> WearableReading:
    """Genera una lectura simulada con escenarios variados."""
    scenario = random.choices(
        ["normal", "elevated_hr", "fall", "low_hr"],
        weights=[70, 15, 5, 10]
    )[0]

    if scenario == "normal":
        hr = random.randint(62, 85)
        ax, ay, az = random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(0.9, 1.1)
        impact = False
    elif scenario == "elevated_hr":
        hr = random.randint(100, 130)
        ax, ay, az = random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), random.uniform(0.8, 1.2)
        impact = False
    elif scenario == "fall":
        hr = random.randint(75, 110)
        ax, ay, az = random.uniform(-3.0, 3.0), random.uniform(-3.0, 3.0), random.uniform(2.5, 4.0)
        impact = True
    else:  # low_hr
        hr = random.randint(42, 49)
        ax, ay, az = random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.uniform(0.9, 1.1)
        impact = False

    return WearableReading(
        heart_rate=hr,
        accel_x=round(ax, 3),
        accel_y=round(ay, 3),
        accel_z=round(az, 3),
        impact_detected=impact,
        timestamp=time.time(),
    )


async def _real_reading(mac: str) -> WearableReading:
    """Lee datos reales del wearable vía BLE (bleak)."""
    try:
        from bleak import BleakClient
        # UUIDs estándar para HR (0x2A37) y acelerómetro varían por dispositivo.
        # Para Mi Band 8 usar miband-python o gadgetbridge protocol.
        async with BleakClient(mac) as client:
            hr_data = await client.read_gatt_char("00002a37-0000-1000-8000-00805f9b34fb")
            hr = hr_data[1] if len(hr_data) > 1 else hr_data[0]
            return WearableReading(
                heart_rate=hr,
                accel_x=0.0, accel_y=0.0, accel_z=1.0,
                impact_detected=False,
                timestamp=time.time(),
            )
    except Exception as e:
        print(f"[BLE] Error leyendo wearable: {e}. Usando mock.")
        return _mock_reading()


def start_publisher(interval_seconds: int = 5):
    """Publica lecturas del wearable a MQTT en loop."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_start()

    print(f"[BLE] Publicando en {MQTT_TOPIC} cada {interval_seconds}s "
          f"({'MOCK' if MOCK_MODE else f'BLE {WEARABLE_MAC}'})")

    try:
        while True:
            if MOCK_MODE:
                reading = _mock_reading()
            else:
                reading = asyncio.run(_real_reading(WEARABLE_MAC))

            payload = json.dumps(asdict(reading))
            client.publish(MQTT_TOPIC, payload)
            print(f"[BLE] FC={reading.heart_rate}bpm  "
                  f"accel=({reading.accel_x},{reading.accel_y},{reading.accel_z})  "
                  f"impacto={reading.impact_detected}")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("[BLE] Detenido.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    start_publisher()
