import json
import os
import threading
import time
from collections import deque
from fastapi import APIRouter
import paho.mqtt.client as mqtt

router = APIRouter(prefix="/alerts", tags=["alerts"])

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MAX_ALERTS = 100

_alerts = deque(maxlen=MAX_ALERTS)
_lock = threading.Lock()


def start_mqtt_listener():
    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            level = data.get("alert_level", "normal")
            if level in ("attention", "emergency"):
                with _lock:
                    _alerts.appendleft({
                        "timestamp": time.time(),
                        "level": level,
                        "heart_rate": data.get("heart_rate"),
                        "impact_detected": data.get("impact_detected", False),
                        "fall_detected": data.get("fall_detected", False),
                    })
        except Exception:
            pass

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
        client.subscribe("samp/wearable")
        t = threading.Thread(target=client.loop_forever, daemon=True)
        t.start()
    except Exception as e:
        print(f"[alerts] MQTT no disponible: {e}")


start_mqtt_listener()


@router.get("")
def get_alerts(limit: int = 50):
    with _lock:
        return list(_alerts)[:limit]


@router.delete("")
def clear_alerts():
    with _lock:
        _alerts.clear()
    return {"ok": True}
