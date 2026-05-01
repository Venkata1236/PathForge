import OnboardingWizard from "../components/OnboardingWizard.jsx";

const OnboardingPage = () => {
  return (
    <div className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 text-center">
          <span className="inline-flex rounded-full bg-emerald-100 px-4 py-1 text-sm font-semibold text-emerald-700">
            PathForge
          </span>
          <h1 className="mt-4 text-4xl font-bold tracking-tight text-slate-900">
            Adaptive learning paths that actually make sense
          </h1>
          <p className="mx-auto mt-3 max-w-2xl text-lg text-slate-600">
            Tell us your current skills, target role, and weekly availability.
            PathForge will generate a practical week-by-week learning roadmap.
          </p>
        </div>
        <OnboardingWizard />
      </div>
    </div>
  );
};

export default OnboardingPage;
