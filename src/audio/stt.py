"""
STT: micrófono USB → texto usando faster-whisper.
MOCK_MODE=true devuelve frases predefinidas sin micrófono.
"""
import os
import random

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny/base/small
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "es")

_MOCK_PHRASES = [
    "Me duele un poco la cabeza",
    "¿Cómo está el tiempo hoy?",
    "Quiero llamar a mi hija",
    "Me siento bien gracias",
    "No tomé la medicación todavía",
    "Tengo sed",
    "¿Qué hora es?",
]

_model = None


def _load_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        print(f"[STT] Cargando modelo Whisper '{WHISPER_MODEL}'...")
        _model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
        print("[STT] Modelo listo.")
    return _model


def transcribe_once() -> str:
    """Graba un fragmento de audio y retorna el texto transcripto."""
    if MOCK_MODE:
        text = random.choice(_MOCK_PHRASES)
        print(f"[STT][MOCK] '{text}'")
        return text

    import sounddevice as sd
    import numpy as np
    import tempfile
    import soundfile as sf

    sample_rate = 16000
    duration = 5  # segundos de grabación
    print("[STT] Escuchando... (5 segundos)")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate,
                   channels=1, dtype="float32")
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, sample_rate)
        model = _load_model()
        segments, _ = model.transcribe(f.name, language=WHISPER_LANGUAGE)
        text = " ".join(seg.text.strip() for seg in segments)

    print(f"[STT] Transcripto: '{text}'")
    return text.strip()
