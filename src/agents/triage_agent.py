"""
Agente de Triage y Emergencia: se activa ante alertas EMERGENCY confirmadas.
Genera el relato situacional y el mensaje para notificar al familiar responsable.
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """Eres el modulo de emergencia de SAMP, un sistema de monitoreo de salud.
Cuando se activa una alerta critica, tenes dos tareas:

1. MENSAJE AL USUARIO: breve, calmante, sin alarmar en exceso. Maximo 2 oraciones.
   Ejemplo: "Detecto algo inusual en tus signos. Ya avise a tu familiar, van a contactarte."

2. RELATO SITUACIONAL para el familiar/cuidador: objetivo, claro y con datos concretos.
   Debe incluir: que se detecto, los valores medidos, hora aproximada, y accion recomendada.
   Ejemplo: "ALERTA: Se detecto una caida con FC=115 bpm y aceleracion de 4.4g a las 14:32.
   La persona no respondio en los ultimos 30 segundos. Se recomienda contacto inmediato."

Separa ambos mensajes con la etiqueta [FAMILIAR].
"""


def run(state: dict) -> dict:
    reading = state["reading"]
    alert = state["alert"]

    hr = reading["heart_rate"]
    impact = reading["impact_detected"]
    reason = alert["reason"]

    user_msg = (
        f"Alerta critica detectada. Datos: FC={hr} bpm, impacto={impact}. "
        f"Motivo: {reason}. "
        f"Genera el mensaje al usuario y el relato situacional para el familiar."
    )

    llm = ChatAnthropic(model=MODEL, max_tokens=400)
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_msg)]
    response = llm.invoke(messages)

    full_text = response.content
    parts = full_text.split("[FAMILIAR]")
    user_msg_out = parts[0].strip()
    family_msg = parts[1].strip() if len(parts) > 1 else ""

    return {
        **state,
        "response": user_msg_out,
        "family_alert": family_msg,
        "agent_used": "triage",
    }
