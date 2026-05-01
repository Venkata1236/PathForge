import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getHistory } from "../services/api.js";

const STATUS_COLORS = {
  "Not Started": "bg-slate-100 text-slate-600",
  "In Progress": "bg-blue-100 text-blue-700",
  "Completed": "bg-emerald-100 text-emerald-700",
};

const HistoryPage = () => {
  const [paths, setPaths] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statuses, setStatuses] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    getHistory()
      .then((res) => setPaths(res.data || []))
      .catch(() => setPaths([]))
      .finally(() => setLoading(false));
  }, []);

  const cycleStatus = (id) => {
    const order = ["Not Started", "In Progress", "Completed"];
    const current = statuses[id] || "Not Started";
    const next = order[(order.indexOf(current) + 1) % order.length];
    setStatuses((prev) => ({ ...prev, [id]: next }));
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-slate-500">Loading history...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <span className="inline-flex rounded-full bg-emerald-100 px-4 py-1 text-sm font-semibold text-emerald-700">
              PathForge
            </span>
            <h1 className="mt-3 text-3xl font-bold text-slate-900">Learning Path History</h1>
            <p className="mt-1 text-slate-500">{paths.length} paths generated</p>
          </div>
          <button
            onClick={() => navigate("/")}
            className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700 transition-colors"
          >
            + New Path
          </button>
        </div>

        {paths.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white py-20 text-center">
            <p className="text-4xl mb-4">📚</p>
            <h3 className="text-lg font-semibold text-slate-800">No paths yet</h3>
            <p className="mt-1 text-sm text-slate-500">Generate your first learning path to see it here.</p>
            <button
              onClick={() => navigate("/")}
              className="mt-6 rounded-xl bg-emerald-600 px-6 py-2 text-sm font-semibold text-white hover:bg-emerald-700 transition-colors"
            >
              Get Started
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {paths.map((path) => {
              const status = statuses[path.session_id] || "Not Started";
              return (
                <div
                  key={path.session_id}
                  className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-semibold text-slate-900">{path.learner_name}</h3>
                        <span className="text-slate-400">→</span>
                        <span className="text-sm font-medium text-emerald-700">{path.target_role}</span>
                      </div>
                      <div className="flex flex-wrap gap-3 text-xs text-slate-500">
                        <span>📅 {new Date(path.created_at).toLocaleDateString()}</span>
                        <span>⏱ {path.total_weeks} weeks</span>
                        <span>📚 {path.course_count} courses</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => cycleStatus(path.session_id)}
                        className={"rounded-full px-3 py-1 text-xs font-semibold cursor-pointer transition-colors " + STATUS_COLORS[status]}
                      >
                        {status}
                      </button>
                      <button
                        onClick={() => navigate("/path", { state: { pathData: path.path_data, learnerProfile: path.path_data } })}
                        className="rounded-xl border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition-colors"
                      >
                        View →
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
