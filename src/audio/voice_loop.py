"""
Loop de conversación por voz: STT → LangGraph → TTS.
Reemplaza chat.py cuando hay micrófono y parlante conectados.
MOCK_MODE=true usa texto de consola + imprime respuestas.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dotenv import load_dotenv
from src.audio.stt import transcribe_once
from src.audio.tts import speak
from src.graph import build_graph
from src.memory.user_profile import load_profile
from src.memory.long_term_memory import LongTermMemory

load_dotenv()

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"
MAX_TURNS = int(os.getenv("MAX_TURNS", "0"))  # 0 = sin límite


def run():
    profile = load_profile()
    memory = LongTermMemory()
    graph = build_graph()
    messages = []
    turn = 0

    name = profile.get("name", "amigo")
    greeting = f"Hola {name}, estoy aquí para acompañarte. ¿Cómo te sentís?"
    speak(greeting)
    print(f"\n[Asistente] {greeting}\n")

    while True:
        if MAX_TURNS and turn >= MAX_TURNS:
            break

        print("[Escuchando...]" if not MOCK_MODE else "[Ingresá texto (Enter para salir)]: ", end="")

        if MOCK_MODE and sys.stdin.isatty():
            user_input = input().strip()
            if not user_input:
                break
        else:
            user_input = transcribe_once()

        if not user_input:
            continue

        print(f"[Usuario] {user_input}")

        rag_context = memory.search(user_input)

        state = {
            "sensor_data": None,
            "alert_level": "normal",
            "user_input": user_input,
            "messages": messages,
            "user_profile": profile,
            "rag_context": rag_context,
        }

        result = graph.invoke(state)
        response = result.get("response", "")
        messages = result.get("messages", messages)

        if response:
            print(f"[Asistente] {response}\n")
            speak(response)
            memory.save(user_input, response)

        turn += 1


if __name__ == "__main__":
    run()
