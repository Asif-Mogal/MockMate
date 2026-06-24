import { LogOut, Sparkles, PlusCircle } from "lucide-react";
import { Link, Outlet, useNavigate } from "react-router-dom";

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
      <header className="border-b border-slate-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-6">
            <Link to="/setup" className="flex items-center gap-3 hover:opacity-90 transition-opacity">
              <div className="grid h-10 w-10 place-items-center rounded bg-ocean text-white">
                <Sparkles size={20} />
              </div>
              <div>
                <p className="text-lg font-bold leading-tight">MockMate</p>
                <p className="text-xs text-slate-500">AI Interview Coach</p>
              </div>
            </Link>
            <nav className="flex items-center border-l border-slate-200 pl-4">
              <Link
                to="/setup"
                className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-ocean transition-all duration-200"
              >
                <PlusCircle size={16} />
                <span>New Session</span>
              </Link>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden text-sm font-medium text-slate-600 sm:inline">{user?.name}</span>
            <button
              className="focus-ring inline-flex h-10 w-10 items-center justify-center rounded border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 hover:text-coral transition-colors"
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
