import axios from 'axios';
import { httpClient } from '../lib/http';
import type {
  ApiErrorDetail,
  RegisterPayload,
  RegisterResponse,
  VerifyEmailResponse,
} from '../types/auth';

export async function registerCustomer(payload: RegisterPayload): Promise<RegisterResponse> {
  const response = await httpClient.post<RegisterResponse>('/api/v1/auth/register', payload);
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

export function extractApiError(error: unknown): {
  message: string;
  fieldErrors: Record<string, string>;
  status?: number;
} {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const detail = (error.response?.data as { detail?: ApiErrorDetail | string } | undefined)
      ?.detail;

    if (typeof detail === 'string') {
      return { message: detail, fieldErrors: {}, status };
    }

    if (detail && typeof detail === 'object') {
      return {
        message: detail.message || 'Vui lòng kiểm tra lại thông tin đã nhập.',
        fieldErrors: detail.field_errors ?? {},
        status,
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
