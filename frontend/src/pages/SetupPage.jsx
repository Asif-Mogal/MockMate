import { Brain, ClipboardList, Gauge } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { api } from "../api/client";

const domains = ["Java", "Spring Boot", "React", "SQL", "DSA", "HR"];
const difficulties = ["Easy", "Medium", "Hard"];
const counts = [5, 10, 15];

export function SetupPage() {
  const navigate = useNavigate();
  const [setup, setSetup] = useState({ domain: "Java", difficulty: "Easy", total_questions: 5 });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const startInterview = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await api.post("/interviews", setup);
      navigate(`/interviews/${response.data.id}/session`);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create interview.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
      <section>
        <h1 className="text-3xl font-bold">Set up your mock interview</h1>
        <p className="mt-2 text-slate-500">Choose the track, pressure level, and length for this practice round.</p>

        <div className="mt-8 space-y-8 rounded bg-white p-6 shadow-panel">
          <OptionGroup icon={<Brain size={20} />} title="Domain" options={domains} value={setup.domain} onChange={(domain) => setSetup({ ...setup, domain })} />
          <OptionGroup icon={<Gauge size={20} />} title="Difficulty" options={difficulties} value={setup.difficulty} onChange={(difficulty) => setSetup({ ...setup, difficulty })} />
          <OptionGroup icon={<ClipboardList size={20} />} title="Questions" options={counts} value={setup.total_questions} onChange={(total_questions) => setSetup({ ...setup, total_questions })} />
          {error && <p className="text-sm text-coral">{error}</p>}
          <button className="focus-ring rounded bg-ocean px-5 py-3 font-semibold text-white hover:bg-cyan-800" onClick={startInterview} disabled={loading}>
            {loading ? "Generating questions..." : "Start interview"}
          </button>
        </div>
      </section>

      <aside className="rounded bg-ink p-6 text-white">
        <p className="text-sm font-semibold uppercase tracking-wide text-cyan-200">Current setup</p>
        <dl className="mt-6 space-y-5">
          <Summary label="Domain" value={setup.domain} />
          <Summary label="Difficulty" value={setup.difficulty} />
          <Summary label="Question count" value={setup.total_questions} />
        </dl>
      </aside>
    </div>
  );
}

function OptionGroup({ icon, title, options, value, onChange }) {
  return (
    <div>
      <div className="mb-3 flex items-center gap-2 font-semibold">{icon}{title}</div>
      <div className="flex flex-wrap gap-3">
        {options.map((option) => (
          <button
            key={option}
            className={`focus-ring rounded border px-4 py-2 ${value === option ? "border-ocean bg-cyan-50 text-ocean" : "border-slate-200 bg-white text-slate-700"}`}
            onClick={() => onChange(option)}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}

function Summary({ label, value }) {
  return (
    <div>
      <dt className="text-sm text-slate-300">{label}</dt>
      <dd className="mt-1 text-2xl font-bold">{value}</dd>
    </div>
  );
}
