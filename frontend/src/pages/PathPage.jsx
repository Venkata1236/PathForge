import { useLocation, useNavigate } from "react-router-dom";
import LearningPathTimeline from "../components/LearningPathTimeline.jsx";
import SkillGapChart from "../components/SkillGapChart.jsx";
import Button from "../components/ui/Button.jsx";

const PathPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { pathData, learnerProfile } = location.state || {};

  if (!pathData) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-slate-600">No learning path found.</p>
          <Button onClick={() => navigate("/")}>Generate a path</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-6 py-10">
      <div className="mx-auto max-w-5xl space-y-10">

        <div className="flex items-start justify-between">
          <div>
            <span className="inline-flex rounded-full bg-emerald-100 px-4 py-1 text-sm font-semibold text-emerald-700">
              PathForge
            </span>
            <h1 className="mt-3 text-3xl font-bold text-slate-900">
              {pathData.learner_name}'s Learning Path
            </h1>
            <p className="mt-1 text-slate-500">
              Target: <strong>{pathData.target_role}</strong> · {pathData.total_weeks} weeks · {learnerProfile?.hours_per_week} hrs/week
            </p>
          </div>
          <Button variant="secondary" onClick={() => navigate("/")}>
            ← New Path
          </Button>
        </div>

        <div className="rounded-2xl bg-white border border-slate-200 p-6 shadow-sm">
          <p className="text-slate-700 leading-relaxed">{pathData.summary}</p>
          <div className="mt-4 flex flex-wrap gap-4 text-sm text-slate-500">
            <span>📚 {pathData.learning_path?.length} courses</span>
            <span>🎯 {pathData.skill_gaps?.length} skill gaps</span>
            <span>⏱ Generated in {pathData.processing_time_seconds}s</span>
          </div>
        </div>

        <SkillGapChart skillGaps={pathData.skill_gaps} />

        <LearningPathTimeline
          weeklySchedule={pathData.weekly_schedule}
          learningPath={pathData.learning_path}
          totalWeeks={pathData.total_weeks}
        />

      </div>
    </div>
  );
};

export default PathPage;
