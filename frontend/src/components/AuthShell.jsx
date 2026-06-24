import { Sparkles } from "lucide-react";

export function AuthShell({ title, subtitle, children }) {
  return (
    <main className="grid min-h-screen bg-paper px-4 py-8 md:grid-cols-[1fr_440px]">
      <section className="hidden items-center justify-center rounded bg-ink p-10 text-white md:flex">
        <div className="max-w-lg">
          <div className="mb-8 grid h-14 w-14 place-items-center rounded bg-ocean">
            <Sparkles size={26} />
          </div>
          <h1 className="text-5xl font-black leading-tight">MockMate</h1>
          <p className="mt-5 text-lg leading-8 text-slate-200">
            Practice real interview questions, answer under pressure, and get precise AI feedback before the real round.
          </p>
        </div>
      </section>
      <section className="flex items-center justify-center">
        <div className="w-full max-w-md rounded bg-white p-8 shadow-panel">
          <h2 className="text-3xl font-bold">{title}</h2>
          <p className="mt-2 text-slate-500">{subtitle}</p>
          {children}
        </div>
      </section>
    </main>
  );
}
