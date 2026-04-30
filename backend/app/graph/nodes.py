"""
PathForge LangGraph Nodes
4 nodes: AssessNode → GapAnalysisNode → PathGeneratorNode → ScheduleBuilderNode
"""

import os
import json
from loguru import logger
from openai import OpenAI
from app.graph.state import PathForgeState
from app.rag.retriever import CourseRetriever
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Singleton retriever — loaded once at startup
_retriever = None

def get_retriever() -> CourseRetriever:
    global _retriever
    if _retriever is None:
        _retriever = CourseRetriever()
    return _retriever


# ─────────────────────────────────────────────
# NODE 1 — AssessNode
# Maps current skills to proficiency levels
# ─────────────────────────────────────────────
def assess_node(state: PathForgeState) -> PathForgeState:
    logger.info(f"[AssessNode] Assessing skills for: {state['learner_name']}")

    prompt = f"""You are a technical skills assessor.

Learner: {state['learner_name']}
Current Skills: {', '.join(state['current_skills'])}
Target Role: {state['target_role']}
Experience Level: {state['experience_level']}

Assess each current skill with a proficiency score (0-100) and identify
what core skills the target role requires.

Return ONLY valid JSON in this exact format:
{{
    "current_skill_levels": {{
        "Python": 75,
        "SQL": 60
    }},
    "role_required_skills": ["skill1", "skill2", "skill3"],
    "learner_summary": "Brief assessment in one sentence"
}}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    assessment = json.loads(response.choices[0].message.content)
    logger.info(f"[AssessNode] Required skills: {assessment.get('role_required_skills', [])}")

    # STATE after Node 1:
    # skill_assessment = {
    #   "current_skill_levels": {"Python": 75, "SQL": 60},
    #   "role_required_skills": ["Machine Learning", "PyTorch", ...],
    #   "learner_summary": "..."
    # }
    return {**state, "skill_assessment": assessment}


# ─────────────────────────────────────────────
# NODE 2 — GapAnalysisNode
# Compares current vs required, ranks gaps
# ─────────────────────────────────────────────
def gap_analysis_node(state: PathForgeState) -> PathForgeState:
    logger.info("[GapAnalysisNode] Identifying skill gaps...")

    assessment = state["skill_assessment"]
    current_skills = assessment.get("current_skill_levels", {})
    required_skills = assessment.get("role_required_skills", [])

    prompt = f"""You are a learning path strategist.

Target Role: {state['target_role']}
Current Skills with Proficiency: {json.dumps(current_skills)}
Required Skills for Role: {required_skills}
Learner Experience: {state['experience_level']}
Hours per Week: {state['hours_per_week']}

Identify the skill gaps and prioritize them:
- Priority 1: Foundation skills (without these, nothing else works)
- Priority 2: Core role-specific skills (most in-demand)
- Priority 3: Supporting skills
- Priority 4: Complementary skills
- Priority 5: Nice-to-have

Rules:
- Only include skills the learner doesn't already have at 70%+ proficiency
- Estimate realistic weeks to fill each gap given {state['hours_per_week']} hours/week
- Maximum 8 gaps total
- If total estimated weeks > 52, keep only priority 1-3 gaps

Return ONLY valid JSON:
{{
    "skill_gaps": [
        {{
            "skill": "Machine Learning",
            "priority": 1,
            "reason": "Core requirement for ML Engineer role",
            "estimated_weeks": 4
        }}
    ]
}}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)
    skill_gaps = result.get("skill_gaps", [])

    # Enforce max 52 weeks guard
    total_weeks = sum(g.get("estimated_weeks", 2) for g in skill_gaps)
    if total_weeks > 52:
        logger.warning(f"[GapAnalysisNode] Total weeks {total_weeks} > 52. Trimming low priority gaps.")
        skill_gaps = [g for g in skill_gaps if g.get("priority", 5) <= 3]

    # Sort by priority
    skill_gaps.sort(key=lambda x: x.get("priority", 5))

    logger.info(f"[GapAnalysisNode] Found {len(skill_gaps)} gaps: {[g['skill'] for g in skill_gaps]}")

    # STATE after Node 2:
    # skill_gaps = [
    #   {"skill": "Machine Learning", "priority": 1, "reason": "...", "estimated_weeks": 4},
    #   ...
    # ]
    return {**state, "skill_gaps": skill_gaps}


# ─────────────────────────────────────────────
# NODE 3 — PathGeneratorNode
# Retrieves courses from FAISS for each gap
# ─────────────────────────────────────────────
def path_generator_node(state: PathForgeState) -> PathForgeState:
    logger.info("[PathGeneratorNode] Retrieving courses for skill gaps...")

    retriever = get_retriever()
    skill_gaps = state["skill_gaps"]
    target_role = state["target_role"]
    experience_level = state["experience_level"]

    all_courses = []
    retrieved_courses = []

    for gap in skill_gaps:
        skill = gap["skill"]
        priority = gap["priority"]

        # Construct targeted FAISS query
        query = f"learn {skill} for {target_role}"
        logger.debug(f"[PathGeneratorNode] FAISS query: '{query}'")

        courses = retriever.search(
            query=query,
            k=2,
            experience_level=experience_level
        )

        for course in courses:
            course["addresses_gap"] = skill
            course["gap_priority"] = priority
            retrieved_courses.append(course)

    # Order courses: prerequisites first (priority 1 gaps first, then 2, 3...)
    retrieved_courses.sort(key=lambda x: x.get("gap_priority", 5))

    # Assign order and week_start placeholder (ScheduleBuilder fills week_start)
    learning_path = []
    for i, course in enumerate(retrieved_courses, 1):
        learning_path.append({
            "order": i,
            "course_name": course["course_name"],
            "institution": course["institution"],
            "level": course["level"],
            "effort": course["effort"],
            "addresses_gap": course["addresses_gap"],
            "week_start": 0  # filled by ScheduleBuilderNode
        })

    logger.info(f"[PathGeneratorNode] Built learning path: {len(learning_path)} courses")

    # STATE after Node 3:
    # learning_path = [
    #   {"order": 1, "course_name": "Intro to ML", "addresses_gap": "Machine Learning", ...},
    #   ...
    # ]
    return {**state, "retrieved_courses": retrieved_courses, "learning_path": learning_path}


# ─────────────────────────────────────────────
# NODE 4 — ScheduleBuilderNode
# Packs courses into weeks, adds milestones
# ─────────────────────────────────────────────
def schedule_builder_node(state: PathForgeState) -> PathForgeState:
    logger.info("[ScheduleBuilderNode] Building weekly schedule...")

    learning_path = state["learning_path"]
    hours_per_week = state["hours_per_week"]
    skill_gaps = state["skill_gaps"]

    # Parse effort string → hours per week (e.g. "2-4 hours per week" → 3)
    def parse_effort(effort_str: str) -> float:
        try:
            nums = [int(s) for s in effort_str.split() if s.isdigit()]
            return sum(nums) / len(nums) if nums else 3.0
        except:
            return 3.0

    weekly_schedule = []
    current_week = 1
    week_courses = []
    week_hours_used = 0
    milestone_counter = 0

    for course in learning_path:
        course_hours = parse_effort(course.get("effort", "3 hours"))

        # If adding this course exceeds capacity, flush current week
        if week_hours_used + course_hours > hours_per_week and week_courses:
            milestone_counter += 1
            milestone = None
            if milestone_counter % 4 == 0:
                gap_index = min(milestone_counter // 4 - 1, len(skill_gaps) - 1)
                gap_skill = skill_gaps[gap_index]["skill"] if skill_gaps else "Skills"
                milestone = f"Milestone: {gap_skill} foundation complete"

            weekly_schedule.append({
                "week": current_week,
                "courses": week_courses.copy(),
                "focus": week_courses[0] if week_courses else "Study",
                "milestone": milestone
            })
            current_week += 1
            week_courses = []
            week_hours_used = 0

        # Update week_start in learning_path
        for item in learning_path:
            if item["course_name"] == course["course_name"] and item["week_start"] == 0:
                item["week_start"] = current_week
                break

        week_courses.append(course["course_name"])
        week_hours_used += course_hours

    # Flush remaining courses
    if week_courses:
        weekly_schedule.append({
            "week": current_week,
            "courses": week_courses.copy(),
            "focus": week_courses[0],
            "milestone": "Milestone: Learning path complete! 🎓"
        })

    total_weeks = current_week

    # Generate summary with GPT
    gap_list = ", ".join([g["skill"] for g in skill_gaps]) if skill_gaps else "key skills"
    prompt = f"""Write a motivating 2-sentence learning path summary.
Learner: {state['learner_name']}
Target Role: {state['target_role']}
Skill Gaps: {gap_list}
Total Weeks: {total_weeks}
Hours/Week: {hours_per_week}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )
    summary = response.choices[0].message.content.strip()

    logger.success(f"[ScheduleBuilderNode] Schedule: {total_weeks} weeks, {len(weekly_schedule)} week blocks")

    # FINAL STATE after Node 4:
    # weekly_schedule, total_weeks, summary all populated
    return {
        **state,
        "learning_path": learning_path,
        "weekly_schedule": weekly_schedule,
        "total_weeks": total_weeks,
        "summary": summary
    }