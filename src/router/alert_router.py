"""
Clasifica una lectura de sensores en tres niveles:
  - normal    → el Agente de Empatía sigue en control
  - attention → el Agente de Vigilancia activa monitoreo reforzado
  - emergency → el Agente de Triaje toma control
"""

from dataclasses import dataclass
from enum import Enum


class AlertLevel(Enum):
    NORMAL = "normal"
    ATTENTION = "attention"
    EMERGENCY = "emergency"


@dataclass
class RouterResult:
    level: AlertLevel
    reason: str
    recommended_agent: str


# Umbrales configurables
HR_HIGH_ATTENTION = 100      # bpm
HR_HIGH_EMERGENCY = 140      # bpm
HR_LOW_ATTENTION = 50        # bpm
INACTIVITY_THRESHOLD_MIN = 30  # minutos sin movimiento (placeholder)
IMPACT_G_THRESHOLD = 2.5     # g para confirmar caída


def _total_acceleration(reading: dict) -> float:
    ax = reading["acceleration_x"]
    ay = reading["acceleration_y"]
    az = reading["acceleration_z"]
    return (ax**2 + ay**2 + az**2) ** 0.5


def classify(reading: dict) -> RouterResult:
    """
    Recibe un dict de SensorReading y devuelve el nivel de alerta.
    La lógica de fusión de sensores (mmWave + wearable) se agregará en Fase 3.
    """
    hr = reading["heart_rate"]
    impact = reading["impact_detected"]
    total_g = _total_acceleration(reading)

    # Caída confirmada: impacto brusco + aceleración total alta
    if impact and total_g > IMPACT_G_THRESHOLD:
        return RouterResult(
            level=AlertLevel.EMERGENCY,
            reason=f"Caída detectada (impacto={impact}, aceleración total={total_g:.2f}g)",
            recommended_agent="triage",
        )

    # FC crítica
    if hr >= HR_HIGH_EMERGENCY:
        return RouterResult(
            level=AlertLevel.EMERGENCY,
            reason=f"FC crítica: {hr} bpm",
            recommended_agent="triage",
        )

    # Posible ataque de pánico o taquicardia moderada
    if hr >= HR_HIGH_ATTENTION:
        return RouterResult(
            level=AlertLevel.ATTENTION,
            reason=f"FC elevada: {hr} bpm — posible pánico o esfuerzo",
            recommended_agent="empathy",
        )

    # Bradicardia
    if hr < HR_LOW_ATTENTION:
        return RouterResult(
            level=AlertLevel.ATTENTION,
            reason=f"FC baja: {hr} bpm",
            recommended_agent="empathy",
        )

    return RouterResult(
        level=AlertLevel.NORMAL,
        reason=f"Parámetros normales (FC={hr} bpm)",
        recommended_agent="empathy",
    )
