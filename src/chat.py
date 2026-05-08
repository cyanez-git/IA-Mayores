"""
SAMP - Fase 2: Loop de conversacion interactiva por consola.
Ejecutar desde la carpeta src/: python -X utf8 chat.py
"""

import random
from pathlib import Path
from dotenv import load_dotenv

from simulator.data_simulator import Scenario, generate
from graph import build_graph
from memory.user_profile import load_profile
from memory.long_term_memory import LongTermMemory

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", override=True)

# Lecturas mayormente normales; 1 de cada 5 genera atencion
_ROUTINE_SCENARIOS = [
    Scenario.NORMAL,
    Scenario.NORMAL,
    Scenario.NORMAL,
    Scenario.NORMAL,
    Scenario.TACHYCARDIA,
]

_STORE_MIN_LEN = 15  # solo guardar mensajes con contenido real


def _print_separator():
    print("-" * 55)


def run():
    profile = load_profile()
    name = profile.get("name", "Usuario")
    memory = LongTermMemory(user_name=name)
    graph = build_graph()
    messages = []

    print("=" * 55)
    print("  SAMP - Sistema de Acompañamiento y Monitoreo Proactivo")
    print("  Fase 2: Conversación interactiva con memoria")
    print("=" * 55)
    print(f"\nHola {name}! Estoy aquí para acompañarte.")
    print('Escribí "salir" en cualquier momento para terminar.\n')

    while True:
        try:
            user_input = input("Vos: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSAMP: Hasta pronto. Cuídate mucho.")
            break

        if user_input.lower() in ("salir", "exit", "quit", "chau", "adios"):
            print("\nSAMP: Fue un gusto charlar. ¡Hasta pronto!")
            break

        # Recuperar memorias relevantes al mensaje actual
        rag_context = memory.retrieve(user_input) if user_input else []

        # Lectura de sensores simulada
        reading = generate(random.choice(_ROUTINE_SCENARIOS))

        state = {
            "reading": reading,
            "alert": {},
            "profile": profile.get("condition", "elder"),
            "user_profile": profile,
            "user_input": user_input,
            "messages": messages,
            "rag_context": rag_context,
            "response": "",
            "family_alert": "",
            "agent_used": "",
        }

        result = graph.invoke(state)

        _print_separator()
        print(f"SAMP: {result['response']}")

        if result.get("family_alert"):
            print(f"\n[ALERTA AL FAMILIAR]\n{result['family_alert']}")

        _print_separator()

        # Actualizar historial de la sesion
        messages = result["messages"]

        # Guardar en memoria larga solo si el mensaje tiene contenido real
        if len(user_input) >= _STORE_MIN_LEN:
            memory.store(
                f"{name} dijo: {user_input}",
                {"type": "conversation", "agent": result["agent_used"]},
            )


if __name__ == "__main__":
    run()
