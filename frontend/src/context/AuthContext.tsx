import {
  type ReactNode,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';
import { setHttpAccessToken, setUnauthorizedHandler } from '../lib/http';
import { logoutUser } from '../services/authApi';
import type { LoginResponse, RegisteredUser, UserRole } from '../types/auth';

const AUTH_STORAGE_KEY = 'emenu_auth_session';

interface StoredAuthSession {
  accessToken: string;
  expiresAt: string;
  redirectPath: string;
  user: RegisteredUser;
}

interface AuthContextValue {
  user: RegisteredUser | null;
  accessToken: string | null;
  expiresAt: string | null;
  isAuthenticated: boolean;
  isLoggingOut: boolean;
  establishSession: (response: LoginResponse, rememberMe: boolean) => void;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function clearStoredAuthSession(): void {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  sessionStorage.removeItem(AUTH_STORAGE_KEY);
}

function readValidStoredSession(): StoredAuthSession | null {
  const raw =
    localStorage.getItem(AUTH_STORAGE_KEY) ?? sessionStorage.getItem(AUTH_STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    const parsed = JSON.parse(raw) as StoredAuthSession;
    const expiryMs = new Date(parsed.expiresAt).getTime();
    if (!parsed.accessToken || !parsed.user || Number.isNaN(expiryMs) || expiryMs <= Date.now()) {
      clearStoredAuthSession();
      return null;
    }
    return parsed;
  } catch {
    clearStoredAuthSession();
    return null;
  }
}

export function getRoleDisplayLabel(role: UserRole): string {
  if (role === 'manager') return 'Quản lý';
  if (role === 'staff') return 'Nhân viên';
  return 'Khách hàng';
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<StoredAuthSession | null>(() => {
    const initial = readValidStoredSession();
    setHttpAccessToken(initial?.accessToken ?? null);
    return initial;
  });
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const clearClientSession = useCallback(() => {
    clearStoredAuthSession();
    setHttpAccessToken(null);
    setSession(null);
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(() => {
      clearClientSession();
    });
    return () => setUnauthorizedHandler(null);
  }, [clearClientSession]);

  // Tự động hủy phiên phía trình duyệt ngay khi chạm thời điểm hết hạn JWT
  useEffect(() => {
    if (!session) return undefined;
    const remainingMs = new Date(session.expiresAt).getTime() - Date.now();
    if (remainingMs <= 0) {
      clearClientSession();
      return undefined;
    }
    const timer = window.setTimeout(() => {
      clearClientSession();
    }, remainingMs);
    return () => window.clearTimeout(timer);
  }, [session, clearClientSession]);

  const establishSession = useCallback((response: LoginResponse, rememberMe: boolean) => {
    const nextSession: StoredAuthSession = {
      accessToken: response.access_token,
      expiresAt: response.expires_at,
      redirectPath: response.redirect_path,
      user: response.user,
    };

    clearStoredAuthSession();
    const storage = rememberMe ? localStorage : sessionStorage;
    storage.setItem(AUTH_STORAGE_KEY, JSON.stringify(nextSession));
    setHttpAccessToken(nextSession.accessToken);
    setSession(nextSession);
  }, []);

  const logout = useCallback(async () => {
    setIsLoggingOut(true);
    try {
      if (session?.accessToken) {
        await logoutUser();
      }
    } catch {
      // Ngay cả khi mạng lỗi hoặc token đã hết hạn, vẫn xóa sạch phiên phía client
    } finally {
      clearClientSession();
      setIsLoggingOut(false);
    }
  }, [session, clearClientSession]);

  const value = useMemo<AuthContextValue>(
    () => ({
      user: session?.user ?? null,
      accessToken: session?.accessToken ?? null,
      expiresAt: session?.expiresAt ?? null,
      isAuthenticated: Boolean(session?.user && session?.accessToken),
      isLoggingOut,
      establishSession,
      logout,
    }),
    [session, isLoggingOut, establishSession, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth phải được sử dụng bên trong AuthProvider.');
  }
  return ctx;
}
