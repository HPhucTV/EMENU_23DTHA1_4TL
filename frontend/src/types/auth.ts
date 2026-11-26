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
  role: 'customer' | 'staff' | 'manager';
  is_active: boolean;
  email_verified: boolean;
  created_at: string;
}

export interface RegisterResponse {
  message: string;
  verification_email_sent: boolean;
  user: RegisteredUser;
}

export interface VerifyEmailResponse {
  message: string;
  email: string;
  email_verified: boolean;
}

export interface ApiErrorDetail {
  code?: string;
  message?: string;
  field_errors?: Record<string, string>;
}
