import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="flex min-h-screen items-center justify-center">Loading MockMate...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
