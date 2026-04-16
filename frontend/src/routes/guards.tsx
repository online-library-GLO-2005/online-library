import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

type Props = {
  children: ReactNode;
};

export function RequireAdmin({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((s) => s.accessToken);
  const isAdmin = useAuthStore((s) => s.is_admin);
  const location = useLocation();

  if (!token || !isAdmin) {
    return <Navigate to="/" replace state={{ from: location }} />;
  }

  return <>{children}</>;
}

export function RequireAuth({ children }: Props) {
  const token = useAuthStore((s) => s.accessToken);
  const location = useLocation();

  if (!token) {
    return <Navigate to="/auth" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}

export function RequireGuest({ children }: Props) {
  const token = useAuthStore((s) => s.accessToken);

  if (token) {
    return <Navigate to="/" replace />;
  }

  return children;
}
