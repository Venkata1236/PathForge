"""
PathForge LangGraph State Schema
TypedDict that flows through all 4 nodes.
"""

from typing import TypedDict, List, Optional


class SkillGap(TypedDict):
    skill: str
    priority: int          # 1 = highest, 5 = lowest
    reason: str
    estimated_weeks: int


class CourseItem(TypedDict):
    order: int
    course_name: str
    institution: str
    level: str
    effort: str
    addresses_gap: str
    week_start: int


class WeeklySchedule(TypedDict):
    week: int
    courses: List[str]
    focus: str
    milestone: Optional[str]


class PathForgeState(TypedDict):
    # ── Input (set by API, never modified by nodes) ──
    learner_name: str
    current_skills: List[str]
    target_role: str
    hours_per_week: int
    experience_level: str     # beginner / intermediate / advanced
    learning_style: str       # structured / flexible / intensive

    # ── Node 1: AssessNode output ──
    skill_assessment: Optional[dict]

    # ── Node 2: GapAnalysisNode output ──
    skill_gaps: Optional[List[SkillGap]]

    # ── Node 3: PathGeneratorNode output ──
    retrieved_courses: Optional[List[dict]]
    learning_path: Optional[List[CourseItem]]

    # ── Node 4: ScheduleBuilderNode output ──
    weekly_schedule: Optional[List[WeeklySchedule]]
    total_weeks: Optional[int]
    summary: Optional[str]