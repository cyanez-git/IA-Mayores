"""
Agente de Empatia: maneja conversacion casual y situaciones de atencion moderada.
Cubre dos perfiles: adulto mayor (compania) y persona con panico/hipocondria (contencion).
"""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

MODEL = "claude-haiku-4-5-20251001"

_BASE_SYSTEM = """Eres SAMP, un asistente de salud y compania inteligente.
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


def _build_system(state: dict) -> str:
    profile = state.get("user_profile", {})
    rag_context = state.get("rag_context", [])

    system = _BASE_SYSTEM

    name = profile.get("name", "")
    age = profile.get("age")
    topics = profile.get("preferences", {}).get("topics", [])
    meds = profile.get("preferences", {}).get("medication_schedule", "")

    if name:
        system += f"\nEl nombre de la persona es {name}."
    if age:
        system += f" Tiene {age} años."
    if topics:
        system += f" Sus temas favoritos son: {', '.join(topics)}."
    if meds:
        system += f" Toma medicación a las {meds}."

    if rag_context:
        system += "\n\nRecuerdos relevantes de conversaciones anteriores:\n"
        system += "\n".join(f"- {m}" for m in rag_context)

    return system


def run(state: dict) -> dict:
    reading = state["reading"]
    alert = state["alert"]
    profile = state.get("profile", "elder")
    user_input = state.get("user_input", "")
    history = state.get("messages", [])

    hr = reading["heart_rate"]
    alert_level = alert["level"]
    reason = alert["reason"]

    system = _build_system(state)
    sensor_note = f"[Sensores: FC={hr} bpm, nivel={alert_level}, {reason}]"

    lc_messages: list = [SystemMessage(content=system + f"\n\n{sensor_note}")]

    # Agregar historial (ultimos 10 turnos para no inflar el context)
    for msg in history[-10:]:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))

    # Mensaje actual del usuario o check-in automático
    if user_input:
        lc_messages.append(HumanMessage(content=user_input))
    elif profile == "panic":
        lc_messages.append(
            HumanMessage(
                content=f"[SAMP inicia contacto: {reason}. Modo CONTENCION.]"
            )
        )
    else:
        lc_messages.append(
            HumanMessage(content=f"[SAMP hace check-in: {reason}]")
        )

    llm = ChatAnthropic(model=MODEL, max_tokens=300)
    response = llm.invoke(lc_messages)

    # Actualizar historial
    new_history = list(history)
    if user_input:
        new_history.append({"role": "user", "content": user_input})
    new_history.append({"role": "assistant", "content": response.content})

    return {
        **state,
        "response": response.content,
        "agent_used": "empathy",
        "messages": new_history,
    }
