export type UserRole = 'customer' | 'staff' | 'manager';

export interface RegisterPayload {
  full_name: string;
  phone: string;
  email: string;
  password: string;
  confirm_password: string;
  accepted_terms: boolean;
}

export interface RegisteredUser {
  id: number;
  full_name: string;
  email: string;
  phone: string;
  role: UserRole;
  is_active: boolean;
  email_verified: boolean;
  created_at: string;
}

export interface RegisterResponse {
  message: string;
  verification_email_sent: boolean;
  user: RegisteredUser;
}

export interface LoginPayload {
  identifier: string;
  password: string;
  remember_me: boolean;
}

export interface LoginResponse {
  message: string;
  access_token: string;
  token_type: 'bearer';
  expires_in: number;
  expires_at: string;
  redirect_path: string;
  user: RegisteredUser;
}

export interface CurrentUserResponse {
  user: RegisteredUser;
  redirect_path: string;
  session_expires_at: string;
}

export interface LogoutResponse {
  message: string;
}

export interface VerifyEmailResponse {
  message: string;
  email: string;
  email_verified: boolean;
}

export interface ForgotPasswordResponse {
  message: string;
  expires_in_minutes: number;
}

export interface ValidateResetTokenResponse {
  valid: boolean;
  message: string;
}

export interface ResetPasswordPayload {
  token: string;
  new_password: string;
  confirm_password: string;
}

export interface ResetPasswordResponse {
  message: string;
  email: string;
}

export interface ApiErrorDetail {
  code?: string;
  message?: string;
  field_errors?: Record<string, string>;
  locked_until?: string;
  retry_after_seconds?: number;
  remaining_attempts?: number;
}
