import { createBrowserRouter, Navigate } from "react-router-dom";

import { AppLayout } from "../components/AppLayout.jsx";
import { ProtectedRoute } from "../components/ProtectedRoute.jsx";
import { LoginPage } from "../pages/LoginPage.jsx";
import { RegisterPage } from "../pages/RegisterPage.jsx";
import { ReportPage } from "../pages/ReportPage.jsx";
import { SetupPage } from "../pages/SetupPage.jsx";
import { SessionPage } from "../pages/SessionPage.jsx";

export const router = createBrowserRouter([
  { path: "/", element: <Navigate to="/setup" replace /> },
  { path: "/login", element: <LoginPage /> },
  { path: "/register", element: <RegisterPage /> },
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      { path: "/setup", element: <SetupPage /> },
      { path: "/interviews/:interviewId/session", element: <SessionPage /> },
      { path: "/interviews/:interviewId/report", element: <ReportPage /> },
    ],
  },
]);
