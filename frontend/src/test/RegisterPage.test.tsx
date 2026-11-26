import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { AxiosError, AxiosHeaders } from 'axios';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { RegisterPage } from '../pages/RegisterPage';
import * as authApi from '../services/authApi';

describe('US-04 RegisterPage UI & Validation', () => {
  it('displays clear Vietnamese validation errors when inputs are invalid', async () => {
    render(
      <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <RegisterPage />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByRole('button', { name: /Tạo tài khoản/i }));

    expect(
      await screen.findByText('Vui lòng nhập họ và tên (ít nhất 2 ký tự).'),
    ).toBeInTheDocument();
    expect(screen.getByText('Vui lòng nhập số điện thoại.')).toBeInTheDocument();
    expect(screen.getByText('Vui lòng nhập địa chỉ email.')).toBeInTheDocument();
    expect(screen.getByText('Mật khẩu phải có ít nhất 8 ký tự.')).toBeInTheDocument();
  });

  it('submits valid registration data and displays email verification notice', async () => {
    const spy = vi.spyOn(authApi, 'registerCustomer').mockResolvedValue({
      message:
        'Đăng ký tài khoản thành công! Vui lòng kiểm tra hộp thư email để xác thực tài khoản.',
      verification_email_sent: true,
      user: {
        id: 1,
        full_name: 'Nguyễn Văn Tiến',
        email: 'tien@vuonpho.vn',
        phone: '0901234567',
        role: 'customer',
        is_active: true,
        email_verified: false,
        created_at: '2026-11-26T16:00:00+07:00',
      },
    });

    render(
      <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <RegisterPage />
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/Họ và tên/i), {
      target: { value: 'Nguyễn Văn Tiến' },
    });
    fireEvent.change(screen.getByLabelText(/Số điện thoại/i), {
      target: { value: '0901234567' },
    });
    fireEvent.change(screen.getByLabelText(/^Email/i), {
      target: { value: 'tien@vuonpho.vn' },
    });
    fireEvent.change(screen.getByLabelText(/^Mật khẩu/i), {
      target: { value: 'VuonPho2026' },
    });
    fireEvent.change(screen.getByLabelText(/Xác nhận mật khẩu/i), {
      target: { value: 'VuonPho2026' },
    });
    fireEvent.click(
      screen.getByRole('checkbox', {
        name: /Tôi đồng ý với Điều khoản sử dụng/i,
      }),
    );

    fireEvent.click(screen.getByRole('button', { name: /Tạo tài khoản/i }));

    expect(await screen.findByText('Kiểm tra hộp thư của bạn')).toBeInTheDocument();
    expect(screen.getByText('tien@vuonpho.vn')).toBeInTheDocument();
    expect(spy).toHaveBeenCalledTimes(1);
  });

  it('highlights duplicate email field error returned by API (409 Conflict)', async () => {
    const axiosConflictError = new AxiosError(
      'Conflict',
      'ERR_BAD_REQUEST',
      undefined,
      undefined,
      {
        status: 409,
        statusText: 'Conflict',
        headers: {},
        config: { headers: new AxiosHeaders() },
        data: {
          detail: {
            code: 'DUPLICATE_ACCOUNT',
            message:
              'Email này đã được đăng ký. Vui lòng đăng nhập hoặc dùng chức năng Quên mật khẩu.',
            field_errors: {
              email:
                'Email này đã được đăng ký. Vui lòng đăng nhập hoặc dùng chức năng Quên mật khẩu.',
            },
          },
        },
      },
    );

    vi.spyOn(authApi, 'registerCustomer').mockRejectedValueOnce(axiosConflictError);

    render(
      <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <RegisterPage />
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/Họ và tên/i), {
      target: { value: 'Nguyễn Văn Khách' },
    });
    fireEvent.change(screen.getByLabelText(/Số điện thoại/i), {
      target: { value: '0987654321' },
    });
    fireEvent.change(screen.getByLabelText(/^Email/i), {
      target: { value: 'trung@vuonpho.vn' },
    });
    fireEvent.change(screen.getByLabelText(/^Mật khẩu/i), {
      target: { value: 'VuonPho2026' },
    });
    fireEvent.change(screen.getByLabelText(/Xác nhận mật khẩu/i), {
      target: { value: 'VuonPho2026' },
    });
    fireEvent.click(
      screen.getByRole('checkbox', {
        name: /Tôi đồng ý với Điều khoản sử dụng/i,
      }),
    );

    fireEvent.click(screen.getByRole('button', { name: /Tạo tài khoản/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(
        'Email này đã được đăng ký',
      );
    });
  });
});
