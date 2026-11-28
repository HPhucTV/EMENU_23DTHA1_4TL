import { type ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ForbiddenPage } from '../pages/ForbiddenPage';
import type { UserRole } from '../types/auth';

interface RoleProtectedRouteProps {
  allowedRoles: UserRole[];
  children: ReactNode;
}

export function RoleProtectedRoute({ allowedRoles, children }: RoleProtectedRouteProps) {
  const { isAuthenticated, user } = useAuth();
  const location = useLocation();

  if (!isAuthenticated || !user) {
    const target = `${location.pathname}${location.search}`;
    return <Navigate to={`/login?next=${encodeURIComponent(target)}`} replace />;
  }

  if (!allowedRoles.includes(user.role)) {
    return <ForbiddenPage />;
  }

  return <>{children}</>;
}
