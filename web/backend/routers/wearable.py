import json
import os
import threading
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import paho.mqtt.client as mqtt

router = APIRouter(prefix="/wearable", tags=["wearable"])

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

_latest = None
_lock = threading.Lock()
_last_seen = None


def start_mqtt_listener():
    def on_message(client, userdata, msg):
        global _latest, _last_seen
        try:
            data = json.loads(msg.payload)
            with _lock:
                _latest = data
                _last_seen = time.time()
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
        print(f"[wearable] MQTT no disponible: {e}")


start_mqtt_listener()


@router.get("/status")
def get_status():
    with _lock:
        connected = _last_seen is not None and (time.time() - _last_seen) < 30
        return {
            "connected": connected,
            "last_seen_seconds_ago": round(time.time() - _last_seen) if _last_seen else None,
            "latest": _latest,
        }


class Thresholds(BaseModel):
    hr_min: int
    hr_max: int


@router.put("/thresholds")
def update_thresholds(t: Thresholds):
    profile_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "data", "profile.json"
    )
    try:
        with open(profile_path) as f:
            profile = json.load(f)
        profile["hr_threshold_low"] = t.hr_min
        profile["hr_threshold_high"] = t.hr_max
        with open(profile_path, "w") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
