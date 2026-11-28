import type { UserRole } from './auth';

export interface StaffAccount {
  id: number;
  full_name: string;
  email: string;
  phone: string;
  role: UserRole;
  is_active: boolean;
  email_verified: boolean;
  failed_login_attempts: number;
  locked_until: string | null;
  created_at: string;
  updated_at: string;
}

export interface StaffListResponse {
  items: StaffAccount[];
  total: number;
  active_count: number;
  locked_count: number;
}

export interface StaffAccountCreatePayload {
  full_name: string;
  phone: string;
  email: string;
  password: string;
  role: 'staff' | 'manager';
}

export interface StaffAccountActionResponse {
  message: string;
  user: StaffAccount;
}

export interface AuditLogItem {
  id: number;
  actor_id: number | null;
  action: string;
  old_value: Record<string, unknown> | null;
  new_value: Record<string, unknown> | null;
  reason: string | null;
  created_at: string;
}

export interface AuditLogListResponse {
  items: AuditLogItem[];
  total: number;
}
