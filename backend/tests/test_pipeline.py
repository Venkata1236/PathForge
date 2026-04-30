import pytest
from app.graph.pipeline import pathforge_pipeline


def get_test_state(name, skills, role, hours, level):
    return {
        "learner_name": name,
        "current_skills": skills,
        "target_role": role,
        "hours_per_week": hours,
        "experience_level": level,
        "learning_style": "structured",
        "skill_assessment": None,
        "skill_gaps": None,
        "retrieved_courses": None,
        "learning_path": None,
        "weekly_schedule": None,
        "total_weeks": None,
        "summary": None
    }


def test_data_analyst_profile():
    result = pathforge_pipeline.invoke(
        get_test_state("Priya", ["Python", "SQL"], "ML Engineer", 8, "intermediate")
    )
    assert result["skill_gaps"] is not None
    assert len(result["skill_gaps"]) > 0
    assert result["total_weeks"] > 0
    assert result["summary"] != ""


def test_beginner_profile():
    result = pathforge_pipeline.invoke(
        get_test_state("Ravi", ["Excel"], "Data Analyst", 5, "beginner")
    )
    assert result["learning_path"] is not None
    assert len(result["learning_path"]) > 0
    assert all(c["effort"] != "Unknown" for c in result["learning_path"])
