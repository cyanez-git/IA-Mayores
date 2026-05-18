import json
import os
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/profile", tags=["profile"])

PROFILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "profile.json"
)


@router.get("")
def get_profile():
    try:
        with open(PROFILE_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")


@router.put("")
def update_profile(data: dict):
    try:
        with open(PROFILE_PATH, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
