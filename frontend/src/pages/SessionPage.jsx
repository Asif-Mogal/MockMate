import { ArrowRight, CheckCircle2 } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { api } from "../api/client";

export function SessionPage() {
  const { interviewId } = useParams();
  const navigate = useNavigate();
  const [interview, setInterview] = useState(null);
  const [answer, setAnswer] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get(`/interviews/${interviewId}`)
      .then((response) => setInterview(response.data))
      .catch(() => setError("Could not load interview."))
      .finally(() => setLoading(false));
  }, [interviewId]);

  const question = interview?.questions?.[currentIndex];
  const answeredCount = useMemo(
    () => interview?.questions?.filter((item) => item.user_answer).length || 0,
    [interview]
  );

  const submitAnswer = async () => {
    if (!answer.trim() || !question) return;
    setSubmitting(true);
    setError("");
    try {
      await api.post(`/interviews/${interviewId}/questions/${question.id}/answer`, { answer });
      
      // Update local state directly so we don't do a full reload/GET request for the interview!
      setInterview((prev) => {
        const updatedQuestions = prev.questions.map((q, idx) => {
          if (idx === currentIndex) {
            return { ...q, user_answer: answer };
          }
          return q;
        });
        return { ...prev, questions: updatedQuestions };
      });
      
      setAnswer("");
      
      // Check if this was the last question
      if (currentIndex + 1 >= interview.questions.length) {
        navigate(`/interviews/${interviewId}/report`);
      } else {
        setCurrentIndex(currentIndex + 1);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Could not save answer.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="p-6 text-center">Loading interview...</div>;
  if (error && !interview) return <p className="text-coral p-6">{error}</p>;

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_340px]">
      <section className="rounded-xl bg-white p-6 shadow-panel border border-slate-100">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-ocean">{interview.domain} · {interview.difficulty}</p>
            <h1 className="mt-2 text-2xl font-bold text-slate-800">Question {currentIndex + 1} of {interview.total_questions}</h1>
          </div>
          <span className="rounded-full bg-cyan-50 border border-cyan-100 px-3 py-1 text-sm font-semibold text-ocean">{answeredCount}/{interview.total_questions} answered</span>
        </div>

        <p className="mt-8 text-xl leading-8 text-slate-700 font-medium">{question.question_text}</p>
        <textarea
          className="focus-ring mt-6 min-h-48 w-full rounded-xl border border-slate-200 p-4 text-slate-700 bg-slate-50/50"
          placeholder="Type your answer here..."
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
        />
        {error && <p className="mt-3 text-sm text-coral">{error}</p>}
        <div className="mt-6 flex flex-wrap gap-3">
          <button 
            className="focus-ring rounded-xl bg-ocean px-6 py-3.5 font-bold text-white hover:bg-cyan-800 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2" 
            onClick={submitAnswer} 
            disabled={submitting || !answer.trim()}
          >
            {submitting ? "Saving..." : (currentIndex + 1 >= interview.questions.length ? "Submit & View Report" : "Save & Next")}
            <ArrowRight size={18} />
          </button>
        </div>
      </section>

      <aside className="rounded-xl bg-white p-6 shadow-panel border border-slate-100 self-start">
        <h2 className="text-lg font-bold text-slate-800 border-b border-slate-100 pb-3">Interview Progress</h2>
        <div className="mt-4 space-y-2">
          {interview.questions.map((q, idx) => {
            const isCurrent = idx === currentIndex;
            const isAnswered = !!q.user_answer;
            return (
              <div 
                key={q.id} 
                className={`flex items-center gap-3 p-3 rounded-lg border transition-all duration-200 ${
                  isCurrent 
                    ? "border-ocean bg-cyan-50/40 text-ocean font-semibold" 
                    : isAnswered 
                      ? "border-slate-50 bg-slate-50/50 text-slate-500" 
                      : "border-transparent text-slate-400"
                }`}
              >
                <div className={`grid h-6 w-6 place-items-center rounded-full text-xs font-bold ${
                  isCurrent 
                    ? "bg-ocean text-white" 
                    : isAnswered 
                      ? "bg-emerald-100 text-emerald-800" 
                      : "bg-slate-100 text-slate-500"
                }`}>
                  {idx + 1}
                </div>
                <div className="flex-1 truncate text-xs">
                  {q.question_text}
                </div>
                {isAnswered && (
                  <CheckCircle2 className="text-emerald-500 shrink-0" size={16} />
                )}
              </div>
            );
          })}
        </div>
      </aside>
    </div>
  );
}
