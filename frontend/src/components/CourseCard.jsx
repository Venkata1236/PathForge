const levelColors = {
  Beginner: "bg-green-100 text-green-700",
  Introductory: "bg-blue-100 text-blue-700",
  Intermediate: "bg-yellow-100 text-yellow-700",
  Advanced: "bg-red-100 text-red-700",
};

const CourseCard = ({ course_name, institution, level, effort, addresses_gap, week_start, order }) => {
  const truncated = course_name?.length > 50 ? course_name.slice(0, 50) + "..." : course_name;
  const levelStyle = levelColors[level] || "bg-slate-100 text-slate-700";

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="mb-3 flex items-start justify-between gap-2">
        <span className="text-xs font-semibold text-slate-400">
          #{ order } · Week { week_start }
        </span>
        <span className={"rounded-full px-2 py-0.5 text-xs font-medium " + levelStyle}>
          {level}
        </span>
      </div>

      <h3 className="mb-1 text-sm font-semibold text-slate-900 leading-snug" title={course_name}>
        {truncated}
      </h3>

      <p className="mb-3 text-xs text-slate-500">{institution}</p>

      <div className="flex flex-wrap gap-2">
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
          {effort}
        </span>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
          Covers: {addresses_gap}
        </span>
      </div>
    </div>
  );
};

export default CourseCard;
