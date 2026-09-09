from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph


class EditorialAgentState(TypedDict, total=False):
    brief: dict[str, Any]
    artifacts: dict[str, Any]
    findings: Annotated[list[dict[str, Any]], operator.add]
    synthesis: dict[str, Any]


def finding(agent: str, gate: str, severity: str, code: str, message: str) -> dict[str, Any]:
    return {"agent": agent, "gate": gate, "severity": severity, "code": code, "message": message, "canApprove": False}


class EditorialAgentSupervisor:
    """Parallel critic graph with a non-approving synthesis node.

    Provider-backed implementations can replace individual critic functions;
    the reducer, state contract and human-gate boundary stay unchanged.
    """

    def __init__(self) -> None:
        graph = StateGraph(EditorialAgentState)
        graph.add_node("education", self._education)
        graph.add_node("subject", self._subject)
        graph.add_node("safety", self._safety)
        graph.add_node("consistency", self._consistency)
        graph.add_node("duplicate", self._duplicate)
        graph.add_node("synthesize", self._synthesize)
        for name in ("education", "subject", "safety", "consistency", "duplicate"):
            graph.add_edge(START, name)
            graph.add_edge(name, "synthesize")
        graph.add_edge("synthesize", END)
        self.graph = graph.compile()

    def run(self, brief: dict[str, Any], artifacts: dict[str, Any]) -> dict[str, Any]:
        state = self.graph.invoke({"brief": brief, "artifacts": artifacts, "findings": []})
        return {"findings": state.get("findings", []), "synthesis": state.get("synthesis", {})}

    @staticmethod
    def _education(state: EditorialAgentState) -> dict[str, Any]:
        present = bool(state.get("brief", {}).get("primaryArea"))
        severity = "info" if present else "blocker"
        return {"findings": [finding("education_critic", "education", severity, "EDU_OBJECTIVE", "A human must confirm one observable primary objective." if present else "The primary learning area is missing.")]}

    @staticmethod
    def _subject(state: EditorialAgentState) -> dict[str, Any]:
        area = state.get("brief", {}).get("primaryArea", "unknown")
        return {"findings": [finding("subject_critic", "subject", "info", "SUBJECT_ACCURACY", f"A qualified reviewer must verify the causal claims for {area}.")]}

    @staticmethod
    def _safety(state: EditorialAgentState) -> dict[str, Any]:
        risk = state.get("brief", {}).get("riskMax", "B")
        severity = "blocker" if risk == "D" else "warning" if risk == "C" else "info"
        message = "Risk D is not eligible for the pilot." if risk == "D" else "Independent safety review is required." if risk == "C" else "Adult controls and stop signals require human verification."
        return {"findings": [finding("safety_critic", "safety", severity, "SAFETY_GATE", message)]}

    @staticmethod
    def _consistency(state: EditorialAgentState) -> dict[str, Any]:
        locales = set(state.get("artifacts", {}).get("localize", {}).get("locales", []))
        severity = "info" if {"en-US", "es-US"}.issubset(locales) else "blocker"
        return {"findings": [finding("consistency_critic", "language", severity, "LOCALE_PARITY", "A bilingual reviewer must confirm meaning and safety parity." if severity == "info" else "Both required locales are not present.")]}

    @staticmethod
    def _duplicate(state: EditorialAgentState) -> dict[str, Any]:
        avoid = state.get("brief", {}).get("avoidMechanisms", [])
        severity = "warning" if avoid else "info"
        return {"findings": [finding("duplicate_critic", "consistency", severity, "CATALOG_NOVELTY", "Compare the mechanism and materials against the listed catalog neighbors.")]}

    @staticmethod
    def _synthesize(state: EditorialAgentState) -> dict[str, Any]:
        findings = state.get("findings", [])
        counts = {level: sum(item["severity"] == level for item in findings) for level in ("blocker", "warning", "info")}
        return {"synthesis": {"counts": counts, "humanGatesRequired": ["education", "subject", "safety", "language", "rights"], "canApprove": False}}
