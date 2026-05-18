import asyncio
import json
import time
import psutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import system, wearable, camera, sensors, profile, alerts

load_dotenv()

app = FastAPI(title="SAMP Admin API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router)
app.include_router(wearable.router)
app.include_router(camera.router)
app.include_router(sensors.router)
app.include_router(profile.router)
app.include_router(alerts.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "SAMP Admin API"}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            mem = psutil.virtual_memory()
            payload = {
                "ts": time.time(),
                "cpu": psutil.cpu_percent(interval=None),
                "ram": mem.percent,
                "wearable": wearable._latest,
                "wearable_connected": (
                    wearable._last_seen is not None
                    and (time.time() - wearable._last_seen) < 30
                ),
                "mmwave": sensors._latest_mmwave,
                "mmwave_active": (
                    sensors._last_seen is not None
                    and (time.time() - sensors._last_seen) < 30
                ),
            }
            await ws.send_text(json.dumps(payload))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
