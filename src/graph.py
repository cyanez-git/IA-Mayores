"""
Grafo LangGraph principal de SAMP.
Flujo: lectura de sensores -> clasificacion -> agente correspondiente.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from router.alert_router import classify, AlertLevel
from agents import empathy_agent, triage_agent


class SAMPState(TypedDict):
    reading: dict
    alert: dict
    profile: str        # "elder" | "panic"
    response: str
    family_alert: str
    agent_used: str


def classify_node(state: SAMPState) -> SAMPState:
    result = classify(state["reading"])
    return {
        **state,
        "alert": {
            "level": result.level.value,
            "reason": result.reason,
            "recommended_agent": result.recommended_agent,
        },
    }


def route(state: SAMPState) -> str:
    return state["alert"]["level"]


def build_graph() -> StateGraph:
    graph = StateGraph(SAMPState)

    graph.add_node("classify", classify_node)
    graph.add_node("empathy", empathy_agent.run)
    graph.add_node("triage", triage_agent.run)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route,
        {
            AlertLevel.NORMAL.value:    "empathy",
            AlertLevel.ATTENTION.value: "empathy",
            AlertLevel.EMERGENCY.value: "triage",
        },
    )

    graph.add_edge("empathy", END)
    graph.add_edge("triage", END)

    return graph.compile()
