import json
from pathlib import Path

PROFILE_PATH = Path(__file__).parent.parent.parent / "data" / "profile.json"

_DEFAULTS = {
    "name": "Usuario",
    "age": None,
    "condition": "elder",
    "family_contact": {},
    "preferences": {},
}


def load_profile() -> dict:
    if PROFILE_PATH.exists():
        return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return _DEFAULTS.copy()


def save_profile(profile: dict) -> None:
    PROFILE_PATH.parent.mkdir(exist_ok=True)
    PROFILE_PATH.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
    )
