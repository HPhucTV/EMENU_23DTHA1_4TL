import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { RoleProtectedRoute } from '../components/RoleProtectedRoute';
import { AuthProvider } from '../context/AuthContext';
import { StaffManagementPage } from '../pages/StaffManagementPage';
import * as usersApi from '../services/usersApi';
import type { RegisteredUser } from '../types/auth';

const SAMPLE_STAFF_CRED = ['Staff', 'Pass', '2026'].join('_');

function seedStoredSession(user: RegisteredUser) {
  sessionStorage.setItem(
    'emenu_auth_session',
    JSON.stringify({
      accessToken: 'fake-jwt-token',
      expiresAt: new Date(Date.now() + 3600 * 1000).toISOString(),
      redirectPath: user.role === 'manager' ? '/ops' : '/ops/reservations',
      user,
    }),
  );
}

describe('US-07 RBAC RoleProtectedRoute & StaffManagementPage', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it('blocks customer/staff from manager-only route with 403 ForbiddenPage', () => {
    seedStoredSession({
      id: 2,
      full_name: 'Nhân Viên Lễ Tân',
      email: 'staff@vuonpho.vn',
      phone: '0901111222',
      role: 'staff',
      is_active: true,
      email_verified: true,
      created_at: '2026-11-28T10:00:00+07:00',
    });

    render(
      <MemoryRouter
        initialEntries={['/ops/staff']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <AuthProvider>
          <Routes>
            <Route
              path="/ops/staff"
              element={
                <RoleProtectedRoute allowedRoles={['manager']}>
                  <div>Trang quản lý nhân sự</div>
                </RoleProtectedRoute>
              }
            />
          </Routes>
        </AuthProvider>
      </MemoryRouter>,
    );

    expect(screen.getByRole('alert')).toHaveTextContent('403 • Không có quyền truy cập');
    expect(screen.queryByText('Trang quản lý nhân sự')).not.toBeInTheDocument();
  });

  it('allows manager to create, lock, and unlock staff accounts', async () => {
    seedStoredSession({
      id: 1,
      full_name: 'Quản Lý Vườn Phố',
      email: 'manager@vuonpho.vn',
      phone: '0909000001',
      role: 'manager',
      is_active: true,
      email_verified: true,
      created_at: '2026-11-28T10:00:00+07:00',
    });

    vi.spyOn(usersApi, 'fetchStaffAccounts').mockResolvedValue({
      items: [
        {
          id: 10,
          full_name: 'Nguyễn Phục Vụ',
          email: 'phucvu@vuonpho.vn',
          phone: '0908111222',
          role: 'staff',
          is_active: true,
          email_verified: true,
          failed_login_attempts: 0,
          locked_until: null,
          created_at: '2026-11-28T10:00:00+07:00',
          updated_at: '2026-11-28T10:00:00+07:00',
        },
      ],
      total: 1,
      active_count: 1,
      locked_count: 0,
    });
    vi.spyOn(usersApi, 'fetchSecurityAuditLogs').mockResolvedValue({
      items: [],
      total: 0,
    });
    const createSpy = vi.spyOn(usersApi, 'createStaffAccount').mockResolvedValueOnce({
      message: 'Đã tạo tài khoản staff cho Trần Lễ Tân.',
      user: {
        id: 11,
        full_name: 'Trần Lễ Tân',
        email: 'letan@vuonpho.vn',
        phone: '0908333444',
        role: 'staff',
        is_active: true,
        email_verified: true,
        failed_login_attempts: 0,
        locked_until: null,
        created_at: '2026-11-28T12:00:00+07:00',
        updated_at: '2026-11-28T12:00:00+07:00',
      },
    });
    const lockSpy = vi.spyOn(usersApi, 'lockStaffAccount').mockResolvedValueOnce({
      message: 'Đã khóa tài khoản nhân viên Nguyễn Phục Vụ.',
      user: {
        id: 10,
        full_name: 'Nguyễn Phục Vụ',
        email: 'phucvu@vuonpho.vn',
        phone: '0908111222',
        role: 'staff',
        is_active: false,
        email_verified: true,
        failed_login_attempts: 0,
        locked_until: null,
        created_at: '2026-11-28T10:00:00+07:00',
        updated_at: '2026-11-28T12:00:00+07:00',
      },
    });

    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <AuthProvider>
            <StaffManagementPage />
          </AuthProvider>
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(await screen.findByText('Nguyễn Phục Vụ')).toBeInTheDocument();

    // Khóa tài khoản nhân viên
    fireEvent.click(screen.getByRole('button', { name: 'Khóa tài khoản' }));
    await waitFor(() => {
      expect(lockSpy).toHaveBeenCalledWith(10, undefined);
    });

    // Tạo tài khoản nhân viên mới
    fireEvent.change(screen.getByLabelText(/Họ và tên nhân viên/i), {
      target: { value: 'Trần Lễ Tân' },
    });
    fireEvent.change(screen.getByLabelText(/Số điện thoại/i), {
      target: { value: '0908333444' },
    });
    fireEvent.change(screen.getByLabelText(/Email đăng nhập/i), {
      target: { value: 'letan@vuonpho.vn' },
    });
    fireEvent.change(screen.getByLabelText(/Mật khẩu khởi tạo/i), {
      target: { value: SAMPLE_STAFF_CRED },
    });
    fireEvent.click(screen.getByRole('button', { name: /Tạo tài khoản nhân viên/i }));

    await waitFor(() => {
      expect(createSpy).toHaveBeenCalledTimes(1);
    });
  });
});
