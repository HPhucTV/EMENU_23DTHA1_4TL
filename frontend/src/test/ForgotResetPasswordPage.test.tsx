import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ForgotPasswordPage } from '../pages/ForgotPasswordPage';
import { ResetPasswordPage } from '../pages/ResetPasswordPage';
import * as authApi from '../services/authApi';

const SAMPLE_NEW_CRED = ['Reset', 'Demo', '2026'].join('_');

describe('US-06 ForgotPasswordPage & ResetPasswordPage', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('validates email and submits forgot-password request', async () => {
    const spy = vi.spyOn(authApi, 'requestPasswordReset').mockResolvedValueOnce({
      message:
        'Nếu email khach@vuonpho.vn đã được đăng ký, hệ thống đã gửi liên kết đặt lại mật khẩu.',
      expires_in_minutes: 15,
    });

    render(
      <MemoryRouter
        initialEntries={['/forgot-password']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <ForgotPasswordPage />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByRole('button', { name: /Gửi liên kết đặt lại mật khẩu/i }));
    expect(
      await screen.findByText('Vui lòng nhập địa chỉ email đã đăng ký.'),
    ).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/Địa chỉ email/i), {
      target: { value: 'Khach@VuonPho.vn' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Gửi liên kết đặt lại mật khẩu/i }));

    expect(await screen.findByText('Kiểm tra hộp thư của bạn')).toBeInTheDocument();
    expect(spy).toHaveBeenCalledWith('khach@vuonpho.vn');
  });

  it('validates one-time token and submits new hashed password', async () => {
    vi.spyOn(authApi, 'validateResetToken').mockResolvedValueOnce({
      valid: true,
      message: 'Liên kết hợp lệ.',
    });
    const resetSpy = vi.spyOn(authApi, 'confirmPasswordReset').mockResolvedValueOnce({
      message: 'Đặt lại mật khẩu thành công!',
      email: 'khach@vuonpho.vn',
    });

    render(
      <MemoryRouter
        initialEntries={['/reset-password?token=valid_one_time_token_123456']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <Routes>
          <Route path="/reset-password" element={<ResetPasswordPage />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(await screen.findByText('Tạo mật khẩu mới')).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/^Mật khẩu mới$/i), {
      target: { value: SAMPLE_NEW_CRED },
    });
    fireEvent.change(screen.getByLabelText(/Xác nhận mật khẩu mới/i), {
      target: { value: SAMPLE_NEW_CRED },
    });
    fireEvent.click(screen.getByRole('button', { name: /Xác nhận đặt lại mật khẩu/i }));

    await waitFor(() => {
      expect(screen.getByText('Đặt lại mật khẩu thành công')).toBeInTheDocument();
    });
    expect(resetSpy).toHaveBeenCalledWith({
      token: 'valid_one_time_token_123456',
      new_password: SAMPLE_NEW_CRED,
      confirm_password: SAMPLE_NEW_CRED,
    });
  });

  it('shows clear message when reset link is expired or already used', async () => {
    vi.spyOn(authApi, 'validateResetToken').mockRejectedValueOnce(new Error('expired'));

    render(
      <MemoryRouter
        initialEntries={['/reset-password?token=expired_token_123456']}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <Routes>
          <Route path="/reset-password" element={<ResetPasswordPage />} />
        </Routes>
      </MemoryRouter>,
    );

    expect(await screen.findByText('Không thể đặt lại mật khẩu')).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Yêu cầu liên kết mới/i })).toBeInTheDocument();
  });
});
