"""
Agente de Empatia: maneja conversacion casual y situaciones de atencion moderada.
Cubre dos perfiles: adulto mayor (compania) y persona con panico/hipocondria (contencion).
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """Eres SAMP, un asistente de salud y compania inteligente.
Tu rol principal es brindar tranquilidad, compania y contencion emocional.

Tenes dos modos segun el contexto que te indiquen:

MODO COMPANIA (adulto mayor):
- Tono calido, paciente y cercano. Usa un lenguaje simple y claro.
- Si los signos vitales son normales, inicia o continua una conversacion amigable.
- Si hay una alerta leve (FC elevada), pregunta con calma como se siente la persona.

MODO CONTENCION (panico/hipocondria):
- Tono calmante y firme. Anclate en datos objetivos para reducir la ansiedad.
- Usa tecnicas de grounding: respiracion 4-7-8, describir el entorno, datos reales de FC.
- Jamas dramatices ni uses lenguaje alarmante.

Reglas generales:
- Respuestas cortas (2-4 oraciones maximo). La persona puede estar estresada.
- Siempre termina con una pregunta o accion concreta para mantener el contacto.
- Nunca diagnostiques. Si algo es serio, deci que vas a avisar a un familiar o medico.
"""


def run(state: dict) -> dict:
    reading = state["reading"]
    alert = state["alert"]
    profile = state.get("profile", "elder")  # "elder" o "panic"

    hr = reading["heart_rate"]
    alert_level = alert["level"]
    reason = alert["reason"]

    if profile == "panic":
        user_msg = (
            f"La persona tiene FC={hr} bpm y reporta angustia. "
            f"Situacion: {reason}. "
            f"Genera una respuesta de contencion en MODO CONTENCION."
        )
    else:
        user_msg = (
            f"La persona tiene FC={hr} bpm. Situacion: {reason}. "
            f"Nivel de alerta: {alert_level}. "
            f"Genera una respuesta apropiada en MODO COMPANIA."
        )

    llm = ChatAnthropic(model=MODEL, max_tokens=300)
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_msg)]
    response = llm.invoke(messages)

    return {**state, "response": response.content, "agent_used": "empathy"}
