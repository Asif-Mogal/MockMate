import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { AuthShell } from "../components/AuthShell.jsx";
import { useAuth } from "../context/AuthContext.jsx";

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    try {
      await register(form.name, form.email, form.password);
      navigate("/setup");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AuthShell title="Create account" subtitle="Start a focused mock interview in minutes.">
      <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
        <input
          className="focus-ring w-full rounded border border-slate-200 px-4 py-3"
          placeholder="Name"
          value={form.name}
          onChange={(event) => setForm({ ...form, name: event.target.value })}
          required
        />
        <input
          className="focus-ring w-full rounded border border-slate-200 px-4 py-3"
          placeholder="Email"
          type="email"
          value={form.email}
          onChange={(event) => setForm({ ...form, email: event.target.value })}
          required
        />
        <input
          className="focus-ring w-full rounded border border-slate-200 px-4 py-3"
          placeholder="Password"
          type="password"
          minLength={8}
          value={form.password}
          onChange={(event) => setForm({ ...form, password: event.target.value })}
          required
        />
        {error && <p className="text-sm text-coral">{error}</p>}
        <button className="focus-ring w-full rounded bg-ocean px-4 py-3 font-semibold text-white hover:bg-cyan-800" disabled={submitting}>
          {submitting ? "Creating..." : "Create account"}
        </button>
      </form>
      <p className="mt-6 text-center text-sm text-slate-500">
        Already registered? <Link className="font-semibold text-ocean" to="/login">Sign in</Link>
      </p>
    </AuthShell>
  );
}
