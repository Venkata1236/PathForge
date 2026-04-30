import time
import uuid
from fastapi import APIRouter, HTTPException
from loguru import logger
from app.models.schemas import LearnerProfileRequest, PathResponse
from app.graph.pipeline import pathforge_pipeline
from app.graph.state import PathForgeState
from app.core.config import settings

router = APIRouter()


@router.post("/generate-path", response_model=PathResponse)
async def generate_path(request: LearnerProfileRequest):
    session_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"[{session_id}] {request.learner_name} → {request.target_role} | {request.experience_level}")

    try:
        initial_state: PathForgeState = {
            "learner_name": request.learner_name,
            "current_skills": request.current_skills,
            "target_role": request.target_role,
            "hours_per_week": request.hours_per_week,
            "experience_level": request.experience_level,
            "learning_style": request.learning_style,
            "skill_assessment": None,
            "skill_gaps": None,
            "retrieved_courses": None,
            "learning_path": None,
            "weekly_schedule": None,
            "total_weeks": None,
            "summary": None
        }

        result = pathforge_pipeline.invoke(initial_state)

        processing_time = round(time.time() - start_time, 2)
        logger.success(f"[{session_id}] Done in {processing_time}s | {result['total_weeks']} weeks")

        return PathResponse(
            session_id=session_id,
            learner_name=result["learner_name"],
            target_role=result["target_role"],
            skill_gaps=result["skill_gaps"] or [],
            learning_path=result["learning_path"] or [],
            weekly_schedule=result["weekly_schedule"] or [],
            total_weeks=result["total_weeks"] or 0,
            summary=result["summary"] or "",
            processing_time_seconds=processing_time
        )

    except Exception as e:
        logger.error(f"[{session_id}] Pipeline error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))