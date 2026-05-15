"""
TTS: texto → voz usando Piper TTS.
MOCK_MODE=true imprime el texto sin audio.
"""
import os
import subprocess
import tempfile

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
# Modelo de voz español: descargarlo con:
#   python -m piper --download-dir models es_ES-davefx-medium
PIPER_MODEL = os.getenv("PIPER_MODEL", "models/es_ES-davefx-medium.onnx")
AUDIO_DEVICE = os.getenv("AUDIO_DEVICE", "default")


def speak(text: str):
    """Convierte texto a voz y lo reproduce."""
    if MOCK_MODE:
        print(f"[TTS][MOCK] 🔊 {text}")
        return

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav_path = f.name

        # Piper genera el WAV, aplay lo reproduce
        subprocess.run(
            ["piper", "--model", PIPER_MODEL, "--output_file", wav_path],
            input=text.encode("utf-8"),
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["aplay", "-D", AUDIO_DEVICE, wav_path],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError:
        print(f"[TTS] Piper no encontrado. Texto: {text}")
    except subprocess.CalledProcessError as e:
        print(f"[TTS] Error: {e}. Texto: {text}")
    finally:
        if os.path.exists(wav_path):
            os.unlink(wav_path)
