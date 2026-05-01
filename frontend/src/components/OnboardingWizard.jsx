import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "./ui/Button.jsx";
import { generatePath } from "../services/api.js";

const roleOptions = [
  "ML Engineer",
  "Data Analyst",
  "Data Scientist",
  "Backend Developer",
  "DevOps Engineer",
];

const skillOptions = [
  "Python",
  "SQL",
  "Excel",
  "Machine Learning",
  "Deep Learning",
  "Docker",
  "Kubernetes",
  "Statistics",
  "Pandas",
  "NumPy",
  "FastAPI",
  "Linux",
];

const OnboardingWizard = () => {
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    learner_name: "",
    current_skills: [],
    target_role: "ML Engineer",
    hours_per_week: 8,
    experience_level: "intermediate",
    learning_style: "structured",
  });

  const loadingMessages = useMemo(
    () => [
      "Analyzing your skills...",
      "Identifying skill gaps...",
      "Finding the best courses...",
      "Building your weekly schedule...",
    ],
    []
  );

  const toggleSkill = (skill) => {
    setForm((prev) => {
      const exists = prev.current_skills.includes(skill);
      return {
        ...prev,
        current_skills: exists
          ? prev.current_skills.filter((item) => item !== skill)
          : [...prev.current_skills, skill].slice(0, 15),
      };
    });
  };

  const updateField = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const nextStep = () => setStep((prev) => Math.min(prev + 1, 3));
  const prevStep = () => setStep((prev) => Math.max(prev - 1, 1));

  const canGoNextStep1 =
    form.learner_name.trim() &&
    form.target_role &&
    form.experience_level &&
    form.learning_style;

  const canGoNextStep2 = form.current_skills.length > 0 && form.hours_per_week >= 2;

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const result = await generatePath(form);
      navigate("/path", { state: { pathData: result, learnerProfile: form } });
    } catch (error) {
      console.error("Path generation failed:", error);
      alert("Failed to generate path. Please check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl rounded-3xl bg-white/90 p-8 shadow-xl backdrop-blur">
      <div className="mb-8">
        <p className="mb-2 text-sm font-medium text-emerald-600">Step {step} of 3</p>
        <h1 className="text-3xl font-bold text-slate-900">Build your personalized learning path</h1>
        <p className="mt-2 text-slate-600">
          Tell PathForge where you are and where you want to go.
        </p>
      </div>

      <div className="mb-8 flex gap-2">
        {[1, 2, 3].map((item) => (
          <div
            key={item}
            className={`h-2 flex-1 rounded-full ${
              item <= step ? "bg-emerald-600" : "bg-slate-200"
            }`}
          />
        ))}
      </div>

      {step === 1 && (
        <div className="space-y-6">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Your name</label>
            <input
              type="text"
              value={form.learner_name}
              onChange={(e) => updateField("learner_name", e.target.value)}
              placeholder="Enter your name"
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">Target role</label>
            <select
              value={form.target_role}
              onChange={(e) => updateField("target_role", e.target.value)}
              className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none transition focus:border-emerald-500"
            >
              {roleOptions.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <label className="mb-3 block text-sm font-medium text-slate-700">
                Experience level
              </label>
              <div className="space-y-2">
                {["beginner", "intermediate", "advanced"].map((level) => (
                  <label
                    key={level}
                    className="flex cursor-pointer items-center gap-3 rounded-xl border border-slate-200 p-3"
                  >
                    <input
                      type="radio"
                      name="experience_level"
                      value={level}
                      checked={form.experience_level === level}
                      onChange={(e) => updateField("experience_level", e.target.value)}
                    />
                    <span className="capitalize text-slate-700">{level}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="mb-3 block text-sm font-medium text-slate-700">
                Learning style
              </label>
              <div className="space-y-2">
                {["structured", "flexible", "intensive"].map((style) => (
                  <label
                    key={style}
                    className="flex cursor-pointer items-center gap-3 rounded-xl border border-slate-200 p-3"
                  >
                    <input
                      type="radio"
                      name="learning_style"
                      value={style}
                      checked={form.learning_style === style}
                      onChange={(e) => updateField("learning_style", e.target.value)}
                    />
                    <span className="capitalize text-slate-700">{style}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-6">
          <div>
            <div className="mb-2 flex items-center justify-between">
              <label className="block text-sm font-medium text-slate-700">Your current skills</label>
              <span className="text-sm text-slate-500">{form.current_skills.length}/15 selected</span>
            </div>

            <div className="flex flex-wrap gap-3">
              {skillOptions.map((skill) => {
                const selected = form.current_skills.includes(skill);
                return (
                  <button
                    key={skill}
                    type="button"
                    onClick={() => toggleSkill(skill)}
                    className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                      selected
                        ? "bg-emerald-600 text-white"
                        : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                    }`}
                  >
                    {skill}
                  </button>
                );
              })}
            </div>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-700">
              Hours per week: {form.hours_per_week}
            </label>
            <input
              type="range"
              min="2"
              max="20"
              step="1"
              value={form.hours_per_week}
              onChange={(e) => updateField("hours_per_week", Number(e.target.value))}
              className="w-full accent-emerald-600"
            />
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="space-y-6">
          <div className="rounded-2xl bg-slate-50 p-6">
            <h2 className="mb-4 text-xl font-semibold text-slate-900">Review your inputs</h2>

            <div className="grid gap-4 md:grid-cols-2">
              <div>
                <p className="text-sm text-slate-500">Name</p>
                <p className="font-medium text-slate-900">{form.learner_name}</p>
              </div>
              <div>
                <p className="text-sm text-slate-500">Target role</p>
                <p className="font-medium text-slate-900">{form.target_role}</p>
              </div>
              <div>
                <p className="text-sm text-slate-500">Experience level</p>
                <p className="font-medium capitalize text-slate-900">{form.experience_level}</p>
              </div>
              <div>
                <p className="text-sm text-slate-500">Learning style</p>
                <p className="font-medium capitalize text-slate-900">{form.learning_style}</p>
              </div>
              <div>
                <p className="text-sm text-slate-500">Hours per week</p>
                <p className="font-medium text-slate-900">{form.hours_per_week}</p>
              </div>
              <div>
                <p className="text-sm text-slate-500">Skills selected</p>
                <p className="font-medium text-slate-900">{form.current_skills.length}</p>
              </div>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              {form.current_skills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700"
                >
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {loading && (
            <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
              <p className="font-semibold text-emerald-700">Generating your path...</p>
              <div className="mt-3 space-y-2 text-sm text-emerald-800">
                {loadingMessages.map((message) => (
                  <p key={message}>{message}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="mt-8 flex items-center justify-between">
        <Button variant="ghost" onClick={prevStep} disabled={step === 1 || loading}>
          Back
        </Button>

        {step < 3 ? (
          <Button
            onClick={nextStep}
            disabled={(step === 1 && !canGoNextStep1) || (step === 2 && !canGoNextStep2)}
          >
            Continue
          </Button>
        ) : (
          <Button onClick={handleSubmit} disabled={loading || !form.learner_name.trim()}>
            {loading ? "Generating..." : "Generate My Path"}
          </Button>
        )}
      </div>
    </div>
  );
};

export default OnboardingWizard;