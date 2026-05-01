import CourseCard from "./CourseCard.jsx";

const phaseConfig = [
  { label: "Foundation", color: "bg-orange-500", text: "text-orange-700", bg: "bg-orange-50", border: "border-orange-200" },
  { label: "Core Skills", color: "bg-blue-500", text: "text-blue-700", bg: "bg-blue-50", border: "border-blue-200" },
  { label: "Advanced", color: "bg-purple-500", text: "text-purple-700", bg: "bg-purple-50", border: "border-purple-200" },
  { label: "Projects", color: "bg-emerald-500", text: "text-emerald-700", bg: "bg-emerald-50", border: "border-emerald-200" },
];

const getPhase = (week, totalWeeks) => {
  const q = totalWeeks / 4;
  if (week <= q) return phaseConfig[0];
  if (week <= q * 2) return phaseConfig[1];
  if (week <= q * 3) return phaseConfig[2];
  return phaseConfig[3];
};

const LearningPathTimeline = ({ weeklySchedule, learningPath, totalWeeks }) => {
  if (!weeklySchedule?.length) return null;

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold text-slate-900">
        Your {totalWeeks}-Week Learning Timeline
      </h2>
      <div className="flex flex-wrap gap-3 mb-4">
        {phaseConfig.map((p) => (
          <span
            key={p.label}
            className={"flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium border " + p.bg + " " + p.text + " " + p.border}
          >
            <span className={"h-2 w-2 rounded-full " + p.color} />
            {p.label}
          </span>
        ))}
      </div>
      <div className="space-y-3">
        {weeklySchedule.map((week) => {
          const phase = getPhase(week.week, totalWeeks);
          const weekCourses = (learningPath || []).filter((c) =>
            (week.courses || []).includes(c.course_name)
          );
          return (
            <div key={week.week} className={"rounded-2xl border p-5 " + phase.bg + " " + phase.border}>
              <div className="mb-3 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className={"flex h-8 w-8 items-center justify-center rounded-full text-sm font-bold text-white " + phase.color}>
                    {week.week}
                  </span>
                  <div>
                    <p className={"text-sm font-semibold " + phase.text}>{phase.label}</p>
                    <p className="text-xs text-slate-500">{week.focus}</p>
                  </div>
                </div>
                {week.milestone && (
                  <span className="flex items-center gap-1 rounded-full bg-yellow-100 px-3 py-1 text-xs font-semibold text-yellow-800">
                    ⭐ Milestone
                  </span>
                )}
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                {weekCourses.map((course) => (
                  <CourseCard key={course.order} {...course} />
                ))}
              </div>
              {week.milestone && (
                <p className="mt-3 text-xs font-medium text-yellow-700 bg-yellow-50 rounded-xl px-3 py-2">
                  {week.milestone}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default LearningPathTimeline;
