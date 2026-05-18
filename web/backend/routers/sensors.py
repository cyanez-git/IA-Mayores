import json
import os
import threading
import time
from fastapi import APIRouter
import paho.mqtt.client as mqtt

router = APIRouter(prefix="/sensors", tags=["sensors"])

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

_latest_mmwave = None
_lock = threading.Lock()
_last_seen = None


def start_mqtt_listener():
    def on_message(client, userdata, msg):
        global _latest_mmwave, _last_seen
        try:
            data = json.loads(msg.payload)
            with _lock:
                _latest_mmwave = data
                _last_seen = time.time()
        except Exception:
            pass

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
        client.subscribe("samp/mmwave")
        t = threading.Thread(target=client.loop_forever, daemon=True)
        t.start()
    except Exception as e:
        print(f"[sensors] MQTT no disponible: {e}")


start_mqtt_listener()


@router.get("/status")
def get_status():
    with _lock:
        active = _last_seen is not None and (time.time() - _last_seen) < 30
        return {
            "mmwave_active": active,
            "last_seen_seconds_ago": round(time.time() - _last_seen) if _last_seen else None,
            "latest": _latest_mmwave,
        }
