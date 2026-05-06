"""
Punto de entrada SAMP - Fase 1 con agentes LangGraph.
Ejecutar desde la carpeta src/: python -X utf8 main.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from simulator.data_simulator import Scenario, generate
from graph import build_graph

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", override=True)

SCENARIOS = [
    (Scenario.NORMAL,       "elder", "Adulto mayor - estado normal"),
    (Scenario.TACHYCARDIA,  "elder", "Adulto mayor - taquicardia leve"),
    (Scenario.PANIC_ATTACK, "panic", "Persona con ataque de panico"),
    (Scenario.FALL,         "elder", "Adulto mayor - caida detectada"),
]


def run():
    graph = build_graph()

    print("=" * 65)
    print("  SAMP - Sistema de Acompanamiento y Monitoreo Proactivo")
    print("  Fase 1: Agentes LangGraph con Claude Haiku")
    print("=" * 65)

    for scenario, profile, label in SCENARIOS:
        reading = generate(scenario)
        print(f"\n{'='*65}")
        print(f"  {label.upper()}")
        print(f"  FC={reading['heart_rate']} bpm | impacto={reading['impact_detected']}")
        print(f"{'='*65}")

        result = graph.invoke({
            "reading": reading,
            "alert": {},
            "profile": profile,
            "response": "",
            "family_alert": "",
            "agent_used": "",
        })

        print(f"[Alerta]  {result['alert']['level'].upper()} - {result['alert']['reason']}")
        print(f"[Agente]  {result['agent_used']}")
        print(f"\n[Respuesta al usuario]\n{result['response']}")

        if result.get("family_alert"):
            print(f"\n[Notificacion al familiar]\n{result['family_alert']}")


if __name__ == "__main__":
    run()
