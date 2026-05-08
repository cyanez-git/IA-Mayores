"""
Tests unitarios del AlertRouter.
Cubre casos normales, límites de FC, detección de caídas y combinaciones de borde.
Ejecutar desde la raíz del proyecto: pytest tests/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from router.alert_router import (
    classify,
    AlertLevel,
    HR_HIGH_ATTENTION,
    HR_HIGH_EMERGENCY,
    HR_LOW_ATTENTION,
    IMPACT_G_THRESHOLD,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def reading(hr: int, impact: bool = False, ax: float = 0.0, ay: float = 0.0, az: float = 1.0) -> dict:
    return {
        "heart_rate": hr,
        "impact_detected": impact,
        "acceleration_x": ax,
        "acceleration_y": ay,
        "acceleration_z": az,
    }


def g_components(total_g: float) -> tuple[float, float, float]:
    """Distribuye total_g en los tres ejes para testear el umbral de aceleracion."""
    per_axis = (total_g ** 2 / 3) ** 0.5
    return per_axis, per_axis, per_axis


# ---------------------------------------------------------------------------
# Casos normales
# ---------------------------------------------------------------------------

class TestNormal:
    def test_fc_minima_normal(self):
        result = classify(reading(hr=HR_LOW_ATTENTION))
        assert result.level == AlertLevel.NORMAL

    def test_fc_maxima_normal(self):
        result = classify(reading(hr=HR_HIGH_ATTENTION - 1))
        assert result.level == AlertLevel.NORMAL

    def test_fc_media(self):
        result = classify(reading(hr=72))
        assert result.level == AlertLevel.NORMAL
        assert result.recommended_agent == "empathy"

    def test_sin_impacto_no_es_caida(self):
        ax, ay, az = g_components(IMPACT_G_THRESHOLD + 1.0)
        result = classify(reading(hr=75, impact=False, ax=ax, ay=ay, az=az))
        assert result.level == AlertLevel.NORMAL


# ---------------------------------------------------------------------------
# Casos de atencion (ATTENTION)
# ---------------------------------------------------------------------------

class TestAttention:
    def test_taquicardia_umbral_exacto(self):
        result = classify(reading(hr=HR_HIGH_ATTENTION))
        assert result.level == AlertLevel.ATTENTION

    def test_taquicardia_moderada(self):
        result = classify(reading(hr=120))
        assert result.level == AlertLevel.ATTENTION
        assert result.recommended_agent == "empathy"

    def test_taquicardia_justo_antes_de_emergencia(self):
        result = classify(reading(hr=HR_HIGH_EMERGENCY - 1))
        assert result.level == AlertLevel.ATTENTION

    def test_bradicardia_umbral_exacto(self):
        result = classify(reading(hr=HR_LOW_ATTENTION - 1))
        assert result.level == AlertLevel.ATTENTION

    def test_bradicardia_valor_bajo(self):
        result = classify(reading(hr=40))
        assert result.level == AlertLevel.ATTENTION
        assert result.recommended_agent == "empathy"


# ---------------------------------------------------------------------------
# Casos de emergencia (EMERGENCY)
# ---------------------------------------------------------------------------

class TestEmergency:
    def test_fc_critica_umbral_exacto(self):
        result = classify(reading(hr=HR_HIGH_EMERGENCY))
        assert result.level == AlertLevel.EMERGENCY
        assert result.recommended_agent == "triage"

    def test_fc_critica_alta(self):
        result = classify(reading(hr=180))
        assert result.level == AlertLevel.EMERGENCY

    def test_caida_confirmada(self):
        ax, ay, az = g_components(IMPACT_G_THRESHOLD + 0.5)
        result = classify(reading(hr=100, impact=True, ax=ax, ay=ay, az=az))
        assert result.level == AlertLevel.EMERGENCY
        assert result.recommended_agent == "triage"
        assert "Caída" in result.reason

    def test_caida_prioridad_sobre_fc_normal(self):
        """Una caída debe dar EMERGENCY aunque la FC sea normal."""
        ax, ay, az = g_components(IMPACT_G_THRESHOLD + 1.0)
        result = classify(reading(hr=70, impact=True, ax=ax, ay=ay, az=az))
        assert result.level == AlertLevel.EMERGENCY


# ---------------------------------------------------------------------------
# Casos de borde (edge cases)
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_impacto_g_insuficiente_no_es_caida(self):
        """Impact=True pero g claramente por debajo del umbral no es caída."""
        # Ponemos todo en un eje para evitar imprecisión de coma flotante
        result = classify(reading(hr=75, impact=True, ax=IMPACT_G_THRESHOLD - 0.1, ay=0.0, az=0.0))
        assert result.level != AlertLevel.EMERGENCY

    def test_impacto_false_g_alto_no_es_emergencia(self):
        """G alto sin flag de impacto no debe ser emergencia por caída."""
        ax, ay, az = g_components(IMPACT_G_THRESHOLD + 2.0)
        result = classify(reading(hr=75, impact=False, ax=ax, ay=ay, az=az))
        assert result.level == AlertLevel.NORMAL

    def test_caida_con_fc_critica_da_emergencia(self):
        """FC crítica + caída: ambos son EMERGENCY; caída se evalúa primero."""
        ax, ay, az = g_components(IMPACT_G_THRESHOLD + 1.0)
        result = classify(reading(hr=HR_HIGH_EMERGENCY + 10, impact=True, ax=ax, ay=ay, az=az))
        assert result.level == AlertLevel.EMERGENCY

    def test_resultado_tiene_razon(self):
        """Todos los resultados deben incluir un motivo no vacío."""
        for hr in [40, 72, 110, 150]:
            result = classify(reading(hr=hr))
            assert result.reason
