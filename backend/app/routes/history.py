"""
PathForge: /history endpoints
"""

from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.get("/history")
async def get_history():
    """Returns all past generated learning paths."""
    logger.info("Fetching learning path history")
    return {"paths": [], "message": "History endpoint — DB wiring in v2"}


@router.get("/history/{session_id}")
async def get_path_by_id(session_id: str):
    """Returns a specific past learning path by session ID."""
    logger.info(f"Fetching path: {session_id}")
    return {"session_id": session_id, "message": "Path detail endpoint — DB wiring in v2"}
