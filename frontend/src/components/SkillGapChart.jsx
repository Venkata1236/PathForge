import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis,
  Tooltip, Cell,
} from "recharts";

const PRIORITY_COLORS = ["#10b981", "#3b82f6", "#8b5cf6", "#f59e0b", "#ef4444"];

const SkillGapChart = ({ skillGaps }) => {
  if (!skillGaps?.length) return null;

  const radarData = skillGaps.map((gap) => ({
    skill: gap.skill.length > 12 ? gap.skill.slice(0, 12) + "..." : gap.skill,
    required: 100,
    current: Math.max(10, 100 - gap.priority * 18),
  }));

  const barData = skillGaps.map((gap) => ({
    skill: gap.skill.length > 16 ? gap.skill.slice(0, 16) + "..." : gap.skill,
    weeks: gap.estimated_weeks,
    priority: gap.priority,
  }));

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-slate-900">Skill Gap Analysis</h2>
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold text-slate-700">Current vs Required Skills</h3>
          <ResponsiveContainer width="100%" height={240}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e2e8f0" />
              <PolarAngleAxis dataKey="skill" tick={{ fontSize: 11, fill: "#64748b" }} />
              <Radar name="Required" dataKey="required" stroke="#e2e8f0" fill="#e2e8f0" fillOpacity={0.4} />
              <Radar name="Current" dataKey="current" stroke="#10b981" fill="#10b981" fillOpacity={0.5} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="mb-4 text-sm font-semibold text-slate-700">Weeks to Fill Each Gap</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={barData} layout="vertical">
              <XAxis type="number" tick={{ fontSize: 11 }} />
              <YAxis type="category" dataKey="skill" tick={{ fontSize: 11, fill: "#64748b" }} width={90} />
              <Tooltip formatter={(v) => [v + " weeks", "Estimated"]} />
              <Bar dataKey="weeks" radius={[0, 6, 6, 0]}>
                {barData.map((entry, i) => (
                  <Cell key={i} fill={PRIORITY_COLORS[(entry.priority - 1) % PRIORITY_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-3 flex flex-wrap gap-2">
            {skillGaps.map((gap, i) => (
              <span key={i} className="flex items-center gap-1 text-xs text-slate-500">
                <span className="h-2 w-2 rounded-full inline-block" style={{ background: PRIORITY_COLORS[(gap.priority - 1) % PRIORITY_COLORS.length] }} />
                P{gap.priority}: {gap.skill}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkillGapChart;
