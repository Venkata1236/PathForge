"""
PathForge LangGraph Edges
Sequential pipeline — no conditional routing needed for v1.
All edges are direct: assess -> gap_analysis -> path_generator -> schedule_builder -> END
"""

from langgraph.graph import END
from app.graph.state import PathForgeState


def should_continue(state: PathForgeState) -> str:
    """
    Future hook for conditional routing.
    e.g. if skill_gaps is empty, skip path_generator and go to END.
    Currently always continues.
    """
    if not state.get("skill_gaps"):
        return END
    return "path_generator"
