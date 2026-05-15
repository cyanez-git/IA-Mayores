"""
Fusión de sensores para detección de caídas.
Confirma caída solo si mmWave + cámara + acelerómetro coinciden.
Evita falsos positivos (agacharse, sentarse bruscamente, etc.)
"""
import time
from dataclasses import dataclass

from src.sensors.mmwave_reader import get_latest as get_mmwave
from src.sensors.camera_feed import get_latest as get_camera

# Umbrales
ACCEL_IMPACT_G = 2.0        # g mínimo para considerar impacto
FALL_CONFIRM_WINDOW = 5.0   # segundos para confirmar la caída post-impacto
CONFIDENCE_THRESHOLD = 0.70 # confianza mínima de MediaPipe


@dataclass
class FallEvent:
    confirmed: bool
    confidence: str    # "high" / "medium" / "low"
    sources: list      # qué sensores lo detectaron
    timestamp: float


def evaluate(accel_x: float, accel_y: float, accel_z: float,
             impact_detected: bool) -> FallEvent:
    """
    Evalúa si hay una caída cruzando los tres sensores.
    Retorna FallEvent con confirmed=True solo si hay evidencia múltiple.
    """
    sources = []
    votes = 0

    # Voto 1: acelerómetro del wearable
    accel_magnitude = (accel_x**2 + accel_y**2 + accel_z**2) ** 0.5
    if impact_detected and accel_magnitude >= ACCEL_IMPACT_G:
        sources.append("acelerometro")
        votes += 1

    # Voto 2: sensor mmWave
    mmwave = get_mmwave()
    if mmwave and mmwave.fall_detected and mmwave.presence_detected:
        sources.append("mmwave")
        votes += 1

    # Voto 3: cámara + MediaPipe
    camera = get_camera()
    if (camera and camera.person_detected
            and not camera.is_standing
            and camera.confidence >= CONFIDENCE_THRESHOLD):
        sources.append("camara")
        votes += 1

    # Requiere al menos 2 de 3 sensores para confirmar
    confirmed = votes >= 2
    if votes == 3:
        confidence = "high"
    elif votes == 2:
        confidence = "medium"
    else:
        confidence = "low"

    return FallEvent(
        confirmed=confirmed,
        confidence=confidence,
        sources=sources,
        timestamp=time.time(),
    )
