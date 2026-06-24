import { AlertTriangle, CheckCircle2, Lightbulb, RotateCcw, Trophy } from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { api } from "../api/client";

const renderBulletPoints = (text, textColorClass) => {
  if (!text) return null;
  
  const sentences = text
    .split(/[.\n]+/)
    .map(s => s.trim())
    .filter(s => s.length > 2);

  if (sentences.length === 0) return null;
  
  if (sentences.length === 1) {
    const cleanText = sentences[0].endsWith('.') ? sentences[0] : `${sentences[0]}.`;
    return <p className={`mt-1.5 text-sm leading-relaxed ${textColorClass}`}>{cleanText}</p>;
  }

  return (
    <ul className="mt-2 space-y-1.5">
      {sentences.map((sentence, idx) => {
        const cleanSentence = sentence.endsWith('.') ? sentence : `${sentence}.`;
        return (
          <li key={idx} className="flex items-start gap-2">
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-slate-400"></span>
            <span className={`text-sm leading-relaxed ${textColorClass}`}>{cleanSentence}</span>
          </li>
        );
      })}
    </ul>
  );
};

export function ReportPage() {
  const { interviewId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get(`/interviews/${interviewId}/report`)
      .then((response) => setReport(response.data))
      .catch(() => setError("Could not load report."))
      .finally(() => setLoading(false));
  }, [interviewId]);

  if (loading) return <div className="p-6 text-center text-slate-600 font-semibold">Building final report... (this may take a few moments)</div>;
  if (error) return <p className="text-coral p-6 text-center font-semibold">{error}</p>;

  return (
    <div className="space-y-6">
      <section className="rounded-xl bg-ink p-6 text-white shadow-panel border border-slate-800">
        <div className="flex flex-wrap items-center justify-between gap-6">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-cyan-200">Final report</p>
            <h1 className="mt-2 text-3xl font-black">{report.placement_readiness}</h1>
          </div>
          <div className="grid h-32 w-32 place-items-center rounded-xl bg-white text-ink shadow-lg">
            <div className="text-center">
              <Trophy className="mx-auto text-ocean" size={28} />
              <p className="mt-2 text-4xl font-black text-slate-800">{report.overall_score}</p>
              <p className="text-xs text-slate-400 font-bold">Overall Score</p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <ReportList title="Strengths" items={report.strengths} variant="strengths" />
        <ReportList title="Weaknesses" items={report.weaknesses} variant="weaknesses" />
        <ReportList title="Recommendations" items={report.recommendations} variant="recommendations" />
      </section>

      <section className="rounded-xl bg-white p-6 shadow-panel border border-slate-100">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <h2 className="text-xl font-bold text-slate-800">Question Review</h2>
          <button 
            className="focus-ring inline-flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2 font-semibold text-slate-700 hover:bg-slate-50 transition-colors duration-200" 
            onClick={() => navigate("/setup")}
          >
            <RotateCcw size={18} /> New interview
          </button>
        </div>
        <div className="mt-5 space-y-6">
          {(() => {
            const parseFeedback = (question) => {
              const critique = question.feedback_critique;
              const improvement = question.feedback_improvement;
              const ideal = question.ideal_answer;

              if (critique || improvement || ideal) {
                return { critique, improvement, ideal };
              }

              const fb = question.feedback || "";
              if (fb.startsWith("Critique:")) {
                const parts1 = fb.split("\n\nHow to Improve:");
                const critiqueText = parts1[0].replace("Critique:", "").trim();
                let improvementText = "";
                let idealText = "";
                if (parts1[1]) {
                  const parts2 = parts1[1].split("\n\nIdeal Answer:");
                  improvementText = parts2[0].trim();
                  if (parts2[1]) {
                    idealText = parts2[1].trim();
                  }
                }
                return {
                  critique: critiqueText || null,
                  improvement: improvementText || null,
                  ideal: idealText || null
                };
              }

              if (fb.includes("Ideal Answer:")) {
                const parts = fb.split("Ideal Answer:");
                const feedbackPart = parts[0].replace("Feedback:", "").trim();
                const idealPart = parts[1].trim();
                return {
                  critique: feedbackPart || null,
                  improvement: null,
                  ideal: idealPart || null
                };
              }

              return {
                critique: fb || null,
                improvement: null,
                ideal: null
              };
            };

            return report.questions.map((question, index) => {
              const { critique, improvement, ideal } = parseFeedback(question);
              return (
                <article className="rounded-xl border border-slate-100 p-6 bg-slate-50/50 shadow-sm" key={question.id}>
                  <div className="flex flex-wrap justify-between gap-3 items-start border-b border-slate-100 pb-3">
                    <h3 className="font-bold text-slate-800 text-base lg:text-lg flex-1">
                      Q{index + 1}. {question.question_text}
                    </h3>
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-black shrink-0 ${
                      question.score >= 80 
                        ? "bg-emerald-100 text-emerald-800" 
                        : question.score >= 50 
                          ? "bg-amber-100 text-amber-800" 
                          : "bg-rose-100 text-rose-800"
                    }`}>
                      {question.score ?? 0}/100
                    </span>
                  </div>
                  
                  <div className="mt-4">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Your Answer</h4>
                    <p className="mt-1.5 text-sm leading-relaxed text-slate-700 bg-white p-3 rounded-lg border border-slate-100 shadow-inner whitespace-pre-wrap">
                      {question.user_answer || "Not answered"}
                    </p>
                  </div>
                  
                  {critique && (
                    <div className="mt-4 bg-blue-50/60 rounded-xl border border-blue-100 p-4">
                      <div className="flex items-center gap-2 text-blue-900 font-bold text-sm">
                        <CheckCircle2 className="text-blue-600 shrink-0" size={16} />
                        <span>Critique & Review</span>
                      </div>
                      {renderBulletPoints(critique, "text-blue-950 font-medium")}
                    </div>
                  )}

                  {improvement && (
                    <div className="mt-4 bg-amber-50/60 rounded-xl border border-amber-100 p-4">
                      <div className="flex items-center gap-2 text-amber-900 font-bold text-sm">
                        <Lightbulb className="text-amber-600 shrink-0" size={16} />
                        <span>How You Could Have Answered</span>
                      </div>
                      {renderBulletPoints(improvement, "text-amber-950 font-medium")}
                    </div>
                  )}

                  {ideal && (
                    <div className="mt-4 bg-emerald-50/40 rounded-xl border border-emerald-100/60 p-4">
                      <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-800">Ideal Answer Reference</h4>
                      <p className="mt-1.5 text-sm leading-relaxed text-emerald-950 bg-white/70 p-3 rounded-lg border border-emerald-100/50">
                        {ideal}
                      </p>
                    </div>
                  )}
                </article>
              );
            });
          })()}
        </div>
      </section>
    </div>
  );
}

function ReportList({ title, items, variant }) {
  const getColors = () => {
    switch (variant) {
      case "strengths":
        return { 
          bg: "bg-emerald-50/50 text-emerald-950 border-emerald-100", 
          icon: <CheckCircle2 className="text-emerald-600 shrink-0" size={18} /> 
        };
      case "weaknesses":
        return { 
          bg: "bg-rose-50/50 text-rose-950 border-rose-100", 
          icon: <AlertTriangle className="text-rose-600 shrink-0" size={18} /> 
        };
      default:
        return { 
          bg: "bg-blue-50/50 text-blue-950 border-blue-100", 
          icon: <Lightbulb className="text-blue-600 shrink-0" size={18} /> 
        };
    }
  };
  
  const colors = getColors();
  
  return (
    <div className="rounded-xl bg-white p-6 shadow-panel border border-slate-100">
      <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">{title}</h2>
      <ul className="mt-4 space-y-3">
        {(items && items.length ? items : ["No items available."]).map((item) => (
          <li className={`flex gap-3 rounded-lg border px-4 py-3 text-sm leading-relaxed ${colors.bg}`} key={item}>
            {colors.icon}
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
