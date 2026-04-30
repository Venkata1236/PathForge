from pydantic import BaseModel, Field
from typing import List, Optional


class LearnerProfileRequest(BaseModel):
    learner_name: str = Field(..., min_length=1, max_length=100)
    current_skills: List[str] = Field(..., min_length=1, max_length=15)
    target_role: str = Field(..., min_length=1)
    hours_per_week: int = Field(..., ge=2, le=40)
    experience_level: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    learning_style: str = Field(..., pattern="^(structured|flexible|intensive)$")

    model_config = {
        "json_schema_extra": {
            "example": {
                "learner_name": "Your Name",      # ← generic
                "current_skills": ["Skill 1", "Skill 2"],
                "target_role": "Target Role",
                "hours_per_week": 8,
                "experience_level": "intermediate",
                "learning_style": "structured"
            }
        }
    }


class SkillGapResponse(BaseModel):
    skill: str
    priority: int
    reason: str
    estimated_weeks: int


class CourseItemResponse(BaseModel):
    order: int
    course_name: str
    institution: str
    level: str
    effort: str
    addresses_gap: str
    week_start: int


class WeeklyScheduleResponse(BaseModel):
    week: int
    courses: List[str]
    focus: str
    milestone: Optional[str]


class PathResponse(BaseModel):
    session_id: str
    learner_name: str
    target_role: str
    skill_gaps: List[SkillGapResponse]
    learning_path: List[CourseItemResponse]
    weekly_schedule: List[WeeklyScheduleResponse]
    total_weeks: int
    summary: str
    processing_time_seconds: float