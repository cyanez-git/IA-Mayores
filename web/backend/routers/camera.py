import os
import subprocess
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/camera", tags=["camera"])

_rtsp_url = os.getenv("RTSP_URL", "rtsp://admin:admin@192.168.1.100:554/stream1")


@router.get("/status")
def get_status():
    global _rtsp_url
    reachable = _check_rtsp(_rtsp_url)
    return {
        "rtsp_url": _rtsp_url,
        "reachable": reachable,
        "mediapipe_active": reachable,
    }


@router.get("/config")
def get_config():
    return {"rtsp_url": _rtsp_url}


class CameraConfig(BaseModel):
    rtsp_url: str


@router.put("/config")
def update_config(config: CameraConfig):
    global _rtsp_url
    _rtsp_url = config.rtsp_url
    return {"ok": True, "rtsp_url": _rtsp_url}


def _check_rtsp(url: str) -> bool:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-rtsp_transport", "tcp",
             "-i", url, "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1"],
            capture_output=True, timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False
