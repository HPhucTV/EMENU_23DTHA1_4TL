import { type FormEvent, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  extractApiError,
  registerCustomer,
  resendVerificationEmail,
} from '../services/authApi';
import type { RegisterPayload, RegisterResponse } from '../types/auth';

const EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const VN_PHONE_PATTERN = /^(0[35789][0-9]{8}|02[0-9]{9})$/;

function normalizePhoneInput(raw: string): string {
  const cleaned = raw.trim().replace(/[\s.\-()]+/g, '');
  if (cleaned.startsWith('+84')) {
    return `0${cleaned.slice(3)}`;
  }
  if (cleaned.startsWith('84') && (cleaned.length === 11 || cleaned.length === 12)) {
    return `0${cleaned.slice(2)}`;
  }
  return cleaned;
}

function validateRegisterForm(values: RegisterPayload): Record<string, string> {
  const errors: Record<string, string> = {};
  const trimmedName = values.full_name.trim().replace(/\s+/g, ' ');
  const normalizedPhone = normalizePhoneInput(values.phone);
  const normalizedEmail = values.email.trim().toLowerCase();

  if (trimmedName.length < 2) {
    errors.full_name = 'Vui lòng nhập họ và tên (ít nhất 2 ký tự).';
  }

  if (!normalizedPhone) {
    errors.phone = 'Vui lòng nhập số điện thoại.';
  } else if (!VN_PHONE_PATTERN.test(normalizedPhone)) {
    errors.phone = 'Số điện thoại không đúng định dạng Việt Nam (ví dụ: 0901234567).';
  }

  if (!normalizedEmail) {
    errors.email = 'Vui lòng nhập địa chỉ email.';
  } else if (!EMAIL_PATTERN.test(normalizedEmail)) {
    errors.email = 'Địa chỉ email không hợp lệ (ví dụ: khach@example.com).';
  }

  if (values.password.length < 8) {
    errors.password = 'Mật khẩu phải có ít nhất 8 ký tự.';
  } else if (!/[A-Za-zÀ-ỹ]/.test(values.password) || !/[0-9]/.test(values.password)) {
    errors.password = 'Mật khẩu phải bao gồm ít nhất 1 chữ cái và 1 chữ số.';
  }

  if (!values.confirm_password) {
    errors.confirm_password = 'Vui lòng nhập lại mật khẩu xác nhận.';
  } else if (values.password !== values.confirm_password) {
    errors.confirm_password = 'Mật khẩu xác nhận không khớp với mật khẩu đã tạo.';
  }

  if (!values.accepted_terms) {
    errors.accepted_terms =
      'Bạn cần đồng ý với Điều khoản sử dụng và Chính sách bảo mật của Vườn Phố.';
  }

  return errors;
}

export function RegisterPage() {
  const [form, setForm] = useState<RegisterPayload>({
    full_name: '',
    phone: '',
    email: '',
    password: '',
    confirm_password: '',
    accepted_terms: false,
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [bannerError, setBannerError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [registeredResult, setRegisteredResult] = useState<RegisterResponse | null>(null);
  const [resendMessage, setResendMessage] = useState<string | null>(null);
  const [isResending, setIsResending] = useState(false);

  const updateField = <K extends keyof RegisterPayload>(key: K, value: RegisterPayload[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
    if (fieldErrors[key]) {
      setFieldErrors((prev) => {
        const next = { ...prev };
        delete next[key];
        return next;
      });
    }
    if (bannerError) {
      setBannerError(null);
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setBannerError(null);

    const clientErrors = validateRegisterForm(form);
    if (Object.keys(clientErrors).length > 0) {
      setFieldErrors(clientErrors);
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await registerCustomer({
        ...form,
        full_name: form.full_name.trim().replace(/\s+/g, ' '),
        phone: normalizePhoneInput(form.phone),
        email: form.email.trim().toLowerCase(),
      });
      setRegisteredResult(response);
      setFieldErrors({});
    } catch (error) {
      const parsed = extractApiError(error);
      setFieldErrors(parsed.fieldErrors);
      setBannerError(parsed.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResendEmail = async () => {
    if (!registeredResult) return;
    setIsResending(true);
    setResendMessage(null);
    try {
      const res = await resendVerificationEmail(registeredResult.user.email);
      setResendMessage(res.message);
    } catch (error) {
      setResendMessage(extractApiError(error).message);
    } finally {
      setIsResending(false);
    }
  };

  return (
    <section className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      <div className="mb-5 lg:hidden">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-brand hover:underline"
        >
          <span aria-hidden="true">←</span>
          <span>Về trang chủ</span>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        {/* Cột trái giới thiệu không gian Vườn Phố trên Desktop (theo Figma 11_dang_ky.png) */}
        <div className="hidden lg:flex lg:col-span-5 rounded-3xl bg-gradient-to-br from-brand via-brand to-brand-dark text-white p-10 flex-col justify-between relative overflow-hidden shadow-sm">
          <div className="relative z-10">
            <p className="text-xs uppercase tracking-[0.2em] text-amber-200/90 font-medium">
              Nhà hàng Ẩm thực Vườn Phố
            </p>
          </div>

          <div className="relative z-10 space-y-5 my-auto py-12">
            <h2 className="font-serif text-4xl xl:text-5xl font-semibold leading-[1.12]">
              Thêm một người bạn,
              <br />
              thêm một cuộc hẹn.
            </h2>
            <p className="text-sm text-stone-200 leading-relaxed max-w-sm">
              Lưu lại những món yêu thích, chủ động đặt bàn và cùng Vườn Phố chuẩn bị bữa ăn tiếp
              theo.
            </p>

            <div className="pt-6 border-t border-white/15 space-y-2 text-xs">
              <p className="uppercase tracking-[0.16em] text-amber-200/90 font-medium">
                Đặt bàn dễ dàng &nbsp;/&nbsp; Chọn món trước
              </p>
              <p className="text-stone-300">Một chốn xanh, vạn vị thân quen.</p>
            </div>
          </div>

          <div
            aria-hidden="true"
            className="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-amber-300/10 blur-2xl"
          />
        </div>

        {/* Cột phải biểu mẫu Đăng ký (theo Figma 11_dang_ky.png & 13_dang_ky_dien_thoai.png) */}
        <div className="lg:col-span-7 rounded-3xl bg-white border border-stone-200/90 p-6 sm:p-10 shadow-sm">
          {/* Thanh chuyển đổi Đăng nhập / Đăng ký */}
          <div className="grid grid-cols-2 rounded-xl bg-cream-subtle p-1.5 text-sm font-medium">
            <Link
              to="/login"
              className="rounded-lg py-2.5 text-center text-stone-600 hover:text-stone-900 transition-colors"
            >
              Đăng nhập
            </Link>
            <span className="rounded-lg bg-white py-2.5 text-center font-semibold text-brand shadow-sm">
              Đăng ký
            </span>
          </div>

          {registeredResult ? (
            <div className="mt-8 space-y-6" role="status">
              <div className="rounded-2xl bg-brand-soft border border-brand/20 p-6 space-y-3">
                <p className="text-xs font-semibold uppercase tracking-wider text-brand">
                  ✓ Tạo tài khoản thành công
                </p>
                <h1 className="font-serif text-3xl font-semibold text-stone-900">
                  Kiểm tra hộp thư của bạn
                </h1>
                <p className="text-sm text-stone-700 leading-relaxed">
                  {registeredResult.message}
                </p>
                <p className="text-sm text-stone-700">
                  Email nhận liên kết xác thực:{' '}
                  <strong className="text-brand">{registeredResult.user.email}</strong>
                </p>
              </div>

              {resendMessage && (
                <p className="rounded-xl bg-cream-subtle px-4 py-3 text-sm text-stone-700">
                  {resendMessage}
                </p>
              )}

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                <Link
                  to="/login"
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand px-6 py-3 text-sm font-semibold text-white hover:bg-brand-dark transition-colors"
                >
                  <span>Đi tới Đăng nhập</span>
                  <span aria-hidden="true">→</span>
                </Link>
                <button
                  type="button"
                  onClick={handleResendEmail}
                  disabled={isResending}
                  className="rounded-xl border border-stone-300 px-5 py-3 text-sm font-medium text-stone-700 hover:border-brand hover:text-brand transition-colors disabled:opacity-60"
                >
                  {isResending ? 'Đang gửi lại...' : 'Gửi lại email xác thực'}
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} noValidate className="mt-8 space-y-5">
              <div>
                <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900">
                  Tạo tài khoản Vườn Phố
                </h1>
                <p className="text-sm text-stone-600 mt-1.5">
                  Bắt đầu những cuộc hẹn ngon cùng người thân.
                </p>
              </div>

              {bannerError && (
                <div
                  role="alert"
                  className="rounded-xl border border-cancel-text/30 bg-cancel-bg px-4 py-3 text-sm text-cancel-text space-y-1"
                >
                  <p className="font-medium">{bannerError}</p>
                  {(fieldErrors.email?.includes('Đăng nhập') ||
                    bannerError.includes('đăng nhập')) && (
                    <p className="text-xs">
                      Đã có tài khoản?{' '}
                      <Link to="/login" className="font-semibold underline">
                        Đăng nhập ngay tại đây
                      </Link>
                    </p>
                  )}
                </div>
              )}

              {/* Họ và tên */}
              <div>
                <label
                  htmlFor="register-full-name"
                  className="block text-xs font-semibold text-stone-800 mb-1.5"
                >
                  Họ và tên <span className="text-cancel-text">*</span>
                </label>
                <input
                  id="register-full-name"
                  name="full_name"
                  type="text"
                  autoComplete="name"
                  placeholder="Nhập họ và tên của bạn"
                  value={form.full_name}
                  onChange={(e) => updateField('full_name', e.target.value)}
                  aria-invalid={Boolean(fieldErrors.full_name)}
                  className={`w-full rounded-xl border px-4 py-3 text-sm bg-white outline-none transition-colors ${
                    fieldErrors.full_name
                      ? 'border-cancel-text focus:border-cancel-text'
                      : 'border-stone-200 focus:border-brand'
                  }`}
                />
                {fieldErrors.full_name && (
                  <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.full_name}</p>
                )}
              </div>

              {/* Số điện thoại & Email (2 cột trên desktop, xếp dọc trên điện thoại) */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label
                    htmlFor="register-phone"
                    className="block text-xs font-semibold text-stone-800 mb-1.5"
                  >
                    Số điện thoại <span className="text-cancel-text">*</span>
                  </label>
                  <input
                    id="register-phone"
                    name="phone"
                    type="tel"
                    autoComplete="tel"
                    placeholder="Nhập số điện thoại"
                    value={form.phone}
                    onChange={(e) => updateField('phone', e.target.value)}
                    aria-invalid={Boolean(fieldErrors.phone)}
                    className={`w-full rounded-xl border px-4 py-3 text-sm bg-white outline-none transition-colors ${
                      fieldErrors.phone
                        ? 'border-cancel-text focus:border-cancel-text'
                        : 'border-stone-200 focus:border-brand'
                    }`}
                  />
                  {fieldErrors.phone && (
                    <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.phone}</p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="register-email"
                    className="block text-xs font-semibold text-stone-800 mb-1.5"
                  >
                    Email <span className="text-cancel-text">*</span>
                  </label>
                  <input
                    id="register-email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    placeholder="Nhập địa chỉ email"
                    value={form.email}
                    onChange={(e) => updateField('email', e.target.value)}
                    aria-invalid={Boolean(fieldErrors.email)}
                    className={`w-full rounded-xl border px-4 py-3 text-sm bg-white outline-none transition-colors ${
                      fieldErrors.email
                        ? 'border-cancel-text focus:border-cancel-text'
                        : 'border-stone-200 focus:border-brand'
                    }`}
                  />
                  {fieldErrors.email && (
                    <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.email}</p>
                  )}
                </div>
              </div>

              {/* Mật khẩu */}
              <div>
                <label
                  htmlFor="register-password"
                  className="block text-xs font-semibold text-stone-800 mb-1.5"
                >
                  Mật khẩu <span className="text-cancel-text">*</span>
                </label>
                <div className="relative">
                  <input
                    id="register-password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="new-password"
                    placeholder="Tạo mật khẩu (tối thiểu 8 ký tự, gồm chữ & số)"
                    value={form.password}
                    onChange={(e) => updateField('password', e.target.value)}
                    aria-invalid={Boolean(fieldErrors.password)}
                    className={`w-full rounded-xl border pl-4 pr-16 py-3 text-sm bg-white outline-none transition-colors ${
                      fieldErrors.password
                        ? 'border-cancel-text focus:border-cancel-text'
                        : 'border-stone-200 focus:border-brand'
                    }`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((prev) => !prev)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-semibold text-brand hover:underline"
                  >
                    {showPassword ? 'Ẩn' : 'Hiện'}
                  </button>
                </div>
                {fieldErrors.password && (
                  <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.password}</p>
                )}
              </div>

              {/* Xác nhận mật khẩu */}
              <div>
                <label
                  htmlFor="register-confirm-password"
                  className="block text-xs font-semibold text-stone-800 mb-1.5"
                >
                  Xác nhận mật khẩu <span className="text-cancel-text">*</span>
                </label>
                <div className="relative">
                  <input
                    id="register-confirm-password"
                    name="confirm_password"
                    type={showConfirmPassword ? 'text' : 'password'}
                    autoComplete="new-password"
                    placeholder="Nhập lại mật khẩu"
                    value={form.confirm_password}
                    onChange={(e) => updateField('confirm_password', e.target.value)}
                    aria-invalid={Boolean(fieldErrors.confirm_password)}
                    className={`w-full rounded-xl border pl-4 pr-16 py-3 text-sm bg-white outline-none transition-colors ${
                      fieldErrors.confirm_password
                        ? 'border-cancel-text focus:border-cancel-text'
                        : 'border-stone-200 focus:border-brand'
                    }`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword((prev) => !prev)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-semibold text-brand hover:underline"
                  >
                    {showConfirmPassword ? 'Ẩn' : 'Hiện'}
                  </button>
                </div>
                {fieldErrors.confirm_password && (
                  <p className="mt-1.5 text-xs text-cancel-text">
                    {fieldErrors.confirm_password}
                  </p>
                )}
              </div>

              <p className="text-xs text-stone-500">
                * Thông tin bắt buộc. Email dùng để xác thực tài khoản.
              </p>

              {/* Điều khoản */}
              <div>
                <label className="flex items-start gap-2.5 text-xs text-stone-600 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={form.accepted_terms}
                    onChange={(e) => updateField('accepted_terms', e.target.checked)}
                    className="mt-0.5 h-4 w-4 rounded border-stone-300 text-brand focus:ring-brand"
                  />
                  <span>
                    Tôi đồng ý với Điều khoản sử dụng và Chính sách bảo mật của Vườn Phố.
                  </span>
                </label>
                {fieldErrors.accepted_terms && (
                  <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.accepted_terms}</p>
                )}
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-brand px-6 py-3.5 text-sm font-semibold text-white hover:bg-brand-dark transition-colors disabled:opacity-60"
              >
                <span>{isSubmitting ? 'Đang tạo tài khoản...' : 'Tạo tài khoản'}</span>
                {!isSubmitting && <span aria-hidden="true">→</span>}
              </button>

              <div className="space-y-2 pt-1 text-xs text-stone-500">
                <p>Bạn sẽ nhận email xác thực sau khi đăng ký.</p>
                <p className="text-stone-700">
                  Đã có tài khoản?{' '}
                  <Link to="/login" className="font-semibold text-brand hover:underline">
                    Đăng nhập
                  </Link>
                </p>
              </div>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
