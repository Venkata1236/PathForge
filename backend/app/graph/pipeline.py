"""
PathForge LangGraph Pipeline
Compiles the 4-node StateGraph.
"""

from langgraph.graph import StateGraph, END
from app.graph.state import PathForgeState
from app.graph.nodes import (
    assess_node,
    gap_analysis_node,
    path_generator_node,
    schedule_builder_node
)
from loguru import logger


def build_pipeline():
    """Build and compile the PathForge StateGraph."""
    workflow = StateGraph(PathForgeState)

    # Register nodes
    workflow.add_node("assess", assess_node)
    workflow.add_node("gap_analysis", gap_analysis_node)
    workflow.add_node("path_generator", path_generator_node)
    workflow.add_node("schedule_builder", schedule_builder_node)

    # Wire edges (sequential — no branching)
    workflow.set_entry_point("assess")
    workflow.add_edge("assess", "gap_analysis")
    workflow.add_edge("gap_analysis", "path_generator")
    workflow.add_edge("path_generator", "schedule_builder")
    workflow.add_edge("schedule_builder", END)

    app = workflow.compile()
    logger.info("PathForge pipeline compiled: assess → gap_analysis → path_generator → schedule_builder → END")
    return app


# Singleton pipeline
pathforge_pipeline = build_pipeline()