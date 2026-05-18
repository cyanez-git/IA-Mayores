import subprocess
import psutil
from fastapi import APIRouter

router = APIRouter(prefix="/system", tags=["system"])


def _service_status(name: str) -> str:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", name],
            capture_output=True, text=True, timeout=3
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


@router.get("/status")
def get_status():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_percent": mem.percent,
        "ram_used_mb": round(mem.used / 1024 / 1024),
        "ram_total_mb": round(mem.total / 1024 / 1024),
        "disk_percent": disk.percent,
        "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 1),
        "uptime_seconds": int(psutil.boot_time()),
    }


@router.get("/services")
def get_services():
    return {
        "mosquitto": _service_status("mosquitto"),
        "ollama": _service_status("ollama"),
        "samp": _service_status("samp"),
        "bluetooth": _service_status("bluetooth"),
    }
