"""
Punto de entrada para la Fase 1: simulación de datos + clasificación de alertas.
Ejecutar: python src/main.py
"""

import json
from simulator.data_simulator import Scenario, generate
from router.alert_router import classify, AlertLevel


SCENARIOS_TO_TEST = [
    Scenario.NORMAL,
    Scenario.TACHYCARDIA,
    Scenario.PANIC_ATTACK,
    Scenario.FALL,
    Scenario.INACTIVITY,
]

LEVEL_ICONS = {
    AlertLevel.NORMAL:    "[OK]",
    AlertLevel.ATTENTION: "[!!]",
    AlertLevel.EMERGENCY: "[SOS]",
}


def run_demo():
    print("=" * 60)
    print("  SAMP — Sistema de Acompañamiento y Monitoreo Proactivo")
    print("  Fase 1: Simulación de datos + Router de alertas")
    print("=" * 60)

    for scenario in SCENARIOS_TO_TEST:
        reading = generate(scenario)
        result = classify(reading)
        icon = LEVEL_ICONS[result.level]

        print(f"\nEscenario : {scenario.value.upper()}")
        print(f"Lectura   : FC={reading['heart_rate']} bpm | "
              f"impacto={reading['impact_detected']}")
        print(f"Resultado : {icon} {result.level.value.upper()} - {result.reason}")
        print(f"Agente    : -> {result.recommended_agent}")

    print("\n" + "=" * 60)
    print("Fase 1 OK. Próximo paso: integración de agentes LangGraph.")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
