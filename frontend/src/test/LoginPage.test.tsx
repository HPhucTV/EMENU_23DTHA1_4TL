import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { AxiosError, AxiosHeaders } from 'axios';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { AuthProvider } from '../context/AuthContext';
import { OperationsLayout } from '../layouts/OperationsLayout';
import { LoginPage } from '../pages/LoginPage';
import * as authApi from '../services/authApi';

const SAMPLE_INPUT = ['Demo', 'Input', '99'].join('_');

describe('US-05 LoginPage, Role Redirect & Logout', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it('validates empty login fields with clear Vietnamese messages', async () => {
    render(
      <MemoryRouter
        initialEntries={['/login']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByRole('button', { name: /Đăng nhập/i }));

    expect(
      await screen.findByText('Vui lòng nhập email hoặc số điện thoại.'),
    ).toBeInTheDocument();
    expect(screen.getByText('Vui lòng nhập mật khẩu.')).toBeInTheDocument();
  });

  it('redirects manager to /ops upon login and revokes session on logout', async () => {
    const futureIso = new Date(Date.now() + 3600 * 1000).toISOString();
    vi.spyOn(authApi, 'loginUser').mockResolvedValueOnce({
      message: 'Đăng nhập thành công!',
      access_token: 'mock-jwt-token',
      token_type: 'bearer',
      expires_in: 3600,
      expires_at: futureIso,
      redirect_path: '/ops',
      user: {
        id: 9,
        full_name: 'Trần Quản Lý',
        email: 'manager@vuonpho.vn',
        phone: '0988555666',
        role: 'manager',
        is_active: true,
        email_verified: true,
        created_at: '2026-11-28T10:00:00+07:00',
      },
    });
    const logoutSpy = vi
      .spyOn(authApi, 'logoutUser')
      .mockResolvedValueOnce({ message: 'Đăng xuất thành công.' });

    render(
      <MemoryRouter
        initialEntries={['/login']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/ops" element={<OperationsLayout />}>
              <Route index element={<div>Bảng điều khiển Quản lý</div>} />
            </Route>
          </Routes>
        </AuthProvider>
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/Email hoặc số điện thoại/i), {
      target: { value: '0988555666' },
    });
    fireEvent.change(screen.getByLabelText(/^Mật khẩu/i), {
      target: { value: SAMPLE_INPUT },
    });

    fireEvent.click(screen.getByRole('button', { name: /Đăng nhập/i }));

    expect(await screen.findByText('Bảng điều khiển Quản lý')).toBeInTheDocument();
    expect(screen.getByText('Trần Quản Lý')).toBeInTheDocument();

    fireEvent.click(screen.getByRole('button', { name: /Đăng xuất/i }));

    await waitFor(() => {
      expect(logoutSpy).toHaveBeenCalledTimes(1);
      expect(screen.getByText('Mừng bạn trở lại')).toBeInTheDocument();
    });
  });

  it('displays 15-minute lockout warning when API returns 423 Locked', async () => {
    const lockedError = new AxiosError('Locked', 'ERR_BAD_REQUEST', undefined, undefined, {
      status: 423,
      statusText: 'Locked',
      headers: {},
      config: { headers: new AxiosHeaders() },
      data: {
        detail: {
          code: 'ACCOUNT_LOCKED',
          message:
            'Bạn đã nhập sai mật khẩu 5 lần liên tiếp. Tài khoản tạm khóa đăng nhập trong 15 phút.',
          locked_until: '2026-11-28T19:45:00+07:00',
          retry_after_seconds: 900,
        },
      },
    });

    vi.spyOn(authApi, 'loginUser').mockRejectedValueOnce(lockedError);

    render(
      <MemoryRouter
        initialEntries={['/login']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/Email hoặc số điện thoại/i), {
      target: { value: 'khach@vuonpho.vn' },
    });
    fireEvent.change(screen.getByLabelText(/^Mật khẩu/i), {
      target: { value: SAMPLE_INPUT },
    });
    fireEvent.click(screen.getByRole('button', { name: /Đăng nhập/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('tạm khóa đăng nhập trong 15 phút');
    });
  });
});
