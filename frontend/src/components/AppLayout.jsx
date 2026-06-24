import { LogOut, Sparkles } from "lucide-react";
import { Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-paper">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded bg-ocean text-white">
              <Sparkles size={20} />
            </div>
            <div>
              <p className="text-lg font-bold">MockMate</p>
              <p className="text-sm text-slate-500">AI Interview Testing Coach</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden text-sm text-slate-600 sm:inline">{user?.name}</span>
            <button
              className="focus-ring inline-flex h-10 w-10 items-center justify-center rounded border border-slate-200 bg-white text-slate-700 hover:bg-slate-50"
              onClick={handleLogout}
              title="Log out"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
