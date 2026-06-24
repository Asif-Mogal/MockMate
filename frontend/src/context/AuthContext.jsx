import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("mockmate_token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(token));

  useEffect(() => {
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    api
      .get("/auth/me")
      .then((response) => setUser(response.data))
      .catch(() => logout())
      .finally(() => setLoading(false));
  }, [token]);

  const login = async (email, password) => {
    const response = await api.post("/auth/login", { email, password });
    localStorage.setItem("mockmate_token", response.data.access_token);
    setToken(response.data.access_token);
  };

  const register = async (name, email, password) => {
    await api.post("/auth/register", { name, email, password });
    await login(email, password);
  };

  const logout = () => {
    localStorage.removeItem("mockmate_token");
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({ token, user, loading, login, register, logout, isAuthenticated: Boolean(token) }),
    [token, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
