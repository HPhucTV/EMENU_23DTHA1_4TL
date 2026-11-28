import axios from 'axios';
import { httpClient } from '../lib/http';
import type {
  ApiErrorDetail,
  CurrentUserResponse,
  ForgotPasswordResponse,
  LoginPayload,
  LoginResponse,
  LogoutResponse,
  RegisterPayload,
  RegisterResponse,
  ResetPasswordPayload,
  ResetPasswordResponse,
  ValidateResetTokenResponse,
  VerifyEmailResponse,
} from '../types/auth';

export async function registerCustomer(payload: RegisterPayload): Promise<RegisterResponse> {
  const response = await httpClient.post<RegisterResponse>('/api/v1/auth/register', payload);
  return response.data;
}

export async function loginUser(payload: LoginPayload): Promise<LoginResponse> {
  const response = await httpClient.post<LoginResponse>('/api/v1/auth/login', payload);
  return response.data;
}

export async function fetchCurrentUser(): Promise<CurrentUserResponse> {
  const response = await httpClient.get<CurrentUserResponse>('/api/v1/auth/me');
  return response.data;
}

export async function logoutUser(): Promise<LogoutResponse> {
  const response = await httpClient.post<LogoutResponse>('/api/v1/auth/logout');
  return response.data;
}

export async function verifyCustomerEmail(token: string): Promise<VerifyEmailResponse> {
  const response = await httpClient.post<VerifyEmailResponse>('/api/v1/auth/verify-email', {
    token,
  });
  return response.data;
}

export async function resendVerificationEmail(email: string): Promise<VerifyEmailResponse> {
  const response = await httpClient.post<VerifyEmailResponse>('/api/v1/auth/resend-verification', {
    email,
  });
  return response.data;
}

export async function requestPasswordReset(email: string): Promise<ForgotPasswordResponse> {
  const response = await httpClient.post<ForgotPasswordResponse>('/api/v1/auth/forgot-password', {
    email,
  });
  return response.data;
}

export async function validateResetToken(token: string): Promise<ValidateResetTokenResponse> {
  const response = await httpClient.get<ValidateResetTokenResponse>(
    '/api/v1/auth/reset-password/validate',
    { params: { token } },
  );
  return response.data;
}

export async function confirmPasswordReset(
  payload: ResetPasswordPayload,
): Promise<ResetPasswordResponse> {
  const response = await httpClient.post<ResetPasswordResponse>(
    '/api/v1/auth/reset-password',
    payload,
  );
  return response.data;
}

export interface ParsedApiError {
  code?: string;
  message: string;
  fieldErrors: Record<string, string>;
  status?: number;
  lockedUntil?: string;
  retryAfterSeconds?: number;
  remainingAttempts?: number;
}

export function extractApiError(error: unknown): ParsedApiError {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const detail = (error.response?.data as { detail?: ApiErrorDetail | string } | undefined)
      ?.detail;

    if (typeof detail === 'string') {
      return { message: detail, fieldErrors: {}, status };
    }

    if (detail && typeof detail === 'object') {
      return {
        code: detail.code,
        message: detail.message || 'Vui lòng kiểm tra lại thông tin đã nhập.',
        fieldErrors: detail.field_errors ?? {},
        status,
        lockedUntil: detail.locked_until,
        retryAfterSeconds: detail.retry_after_seconds,
        remainingAttempts: detail.remaining_attempts,
      };
    }

    return {
      message: 'Không thể kết nối máy chủ. Vui lòng thử lại sau giây lát.',
      fieldErrors: {},
      status,
    };
  }

  return {
    message: 'Đã xảy ra lỗi không xác định. Vui lòng thử lại.',
    fieldErrors: {},
  };
}
