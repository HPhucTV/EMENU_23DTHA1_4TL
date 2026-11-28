import { httpClient } from '../lib/http';
import type {
  AuditLogListResponse,
  StaffAccountActionResponse,
  StaffAccountCreatePayload,
  StaffListResponse,
} from '../types/users';

export async function fetchStaffAccounts(params?: {
  search?: string;
  status_filter?: 'active' | 'locked';
}): Promise<StaffListResponse> {
  const response = await httpClient.get<StaffListResponse>('/api/v1/users/staff', {
    params,
  });
  return response.data;
}

export async function createStaffAccount(
  payload: StaffAccountCreatePayload,
): Promise<StaffAccountActionResponse> {
  const response = await httpClient.post<StaffAccountActionResponse>(
    '/api/v1/users/staff',
    payload,
  );
  return response.data;
}

export async function lockStaffAccount(
  userId: number,
  reason?: string,
): Promise<StaffAccountActionResponse> {
  const response = await httpClient.patch<StaffAccountActionResponse>(
    `/api/v1/users/staff/${userId}/lock`,
    reason ? { reason } : {},
  );
  return response.data;
}

export async function unlockStaffAccount(
  userId: number,
): Promise<StaffAccountActionResponse> {
  const response = await httpClient.patch<StaffAccountActionResponse>(
    `/api/v1/users/staff/${userId}/unlock`,
  );
  return response.data;
}

export async function fetchSecurityAuditLogs(limit = 20): Promise<AuditLogListResponse> {
  const response = await httpClient.get<AuditLogListResponse>('/api/v1/users/audit-logs', {
    params: { limit },
  });
  return response.data;
}
