import { type FormEvent, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { formatDateTimeGMT7 } from '../lib/formatters';
import { extractApiError, loginUser } from '../services/authApi';

const EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const VN_PHONE_PATTERN = /^(0[35789][0-9]{8}|02[0-9]{9})$/;

function normalizeIdentifierInput(raw: string): { valid: boolean; normalized: string; error?: string } {
  const trimmed = raw.trim();
  if (!trimmed) {
    return {
      valid: false,
      normalized: '',
      error: 'Vui lòng nhập email hoặc số điện thoại.',
    };
  }

  if (trimmed.includes('@')) {
    const email = trimmed.toLowerCase();
    if (!EMAIL_PATTERN.test(email)) {
      return {
        valid: false,
        normalized: email,
        error: 'Địa chỉ email đăng nhập không đúng định dạng.',
      };
    }
    return { valid: true, normalized: email };
  }

  let phone = trimmed.replace(/[\s.\-()]+/g, '');
  if (phone.startsWith('+84')) {
    phone = `0${phone.slice(3)}`;
  } else if (phone.startsWith('84') && (phone.length === 11 || phone.length === 12)) {
    phone = `0${phone.slice(2)}`;
  }

  if (!VN_PHONE_PATTERN.test(phone)) {
    return {
      valid: false,
      normalized: phone,
      error: 'Vui lòng nhập đúng email hoặc số điện thoại Việt Nam (ví dụ: 0901234567).',
    };
  }
  return { valid: true, normalized: phone };
}

function resolveSafeNextPath(nextParam: string | null, defaultRedirectPath: string): string {
  if (
    nextParam &&
    nextParam.startsWith('/') &&
    !nextParam.startsWith('//') &&
    !nextParam.startsWith('/login') &&
    !nextParam.startsWith('/register')
  ) {
    return nextParam;
  }
  return defaultRedirectPath;
}

export function LoginPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { establishSession } = useAuth();

  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [bannerError, setBannerError] = useState<string | null>(null);
  const [lockedUntil, setLockedUntil] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setBannerError(null);
    setLockedUntil(null);

    const nextFieldErrors: Record<string, string> = {};
    const identifierCheck = normalizeIdentifierInput(identifier);
    if (!identifierCheck.valid && identifierCheck.error) {
      nextFieldErrors.identifier = identifierCheck.error;
    }
    if (!password.trim()) {
      nextFieldErrors.password = 'Vui lòng nhập mật khẩu.';
    }

    if (Object.keys(nextFieldErrors).length > 0) {
      setFieldErrors(nextFieldErrors);
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await loginUser({
        identifier: identifierCheck.normalized,
        password,
        remember_me: rememberMe,
      });

      establishSession(response, rememberMe);
      const targetPath = resolveSafeNextPath(
        searchParams.get('next'),
        response.redirect_path,
      );
      navigate(targetPath, { replace: true });
    } catch (error) {
      const parsed = extractApiError(error);
      setFieldErrors(parsed.fieldErrors);
      setBannerError(parsed.message);
      if (parsed.status === 423 && parsed.lockedUntil) {
        setLockedUntil(parsed.lockedUntil);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      {/* Liên kết quay về trang chủ trên điện thoại (theo Figma 12_dang_nhap_dien_thoai.png) */}
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
        {/* Cột trái giới thiệu trên Desktop (theo Figma 10_dang_nhap.png) */}
        <div className="hidden lg:flex lg:col-span-5 rounded-3xl bg-gradient-to-br from-brand via-brand to-brand-dark text-white p-10 flex-col justify-between relative overflow-hidden shadow-sm">
          <div className="relative z-10">
            <p className="text-xs uppercase tracking-[0.2em] text-amber-200/90 font-medium">
              Nhà hàng Ẩm thực Vườn Phố
            </p>
          </div>

          <div className="relative z-10 space-y-5 my-auto py-12">
            <h2 className="font-serif text-4xl xl:text-5xl font-semibold leading-[1.12]">
              Chào bạn,
              <br />
              mời ghé vườn.
            </h2>
            <p className="text-sm text-stone-200 leading-relaxed max-w-sm">
              Một tài khoản cho những bữa ăn thân quen.
              <br />
              Đặt bàn, chọn món và an tâm chờ ngày hẹn.
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

        {/* Cột phải biểu mẫu Đăng nhập (theo Figma 10_dang_nhap.png & 12_dang_nhap_dien_thoai.png) */}
        <div className="lg:col-span-7 rounded-3xl bg-white border border-stone-200/90 p-6 sm:p-10 shadow-sm">
          {/* Thanh chuyển đổi Đăng nhập / Đăng ký */}
          <div className="grid grid-cols-2 rounded-xl bg-cream-subtle p-1.5 text-sm font-medium">
            <span className="rounded-lg bg-white py-2.5 text-center font-semibold text-brand shadow-sm">
              Đăng nhập
            </span>
            <Link
              to="/register"
              className="rounded-lg py-2.5 text-center text-stone-600 hover:text-stone-900 transition-colors"
            >
              Đăng ký
            </Link>
          </div>

          <form onSubmit={handleSubmit} noValidate className="mt-8 space-y-5">
            <div>
              <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900">
                Mừng bạn trở lại
              </h1>
              <p className="text-sm text-stone-600 mt-1.5">
                Đăng nhập để đặt bàn, chọn món trước và quản lý cuộc hẹn.
              </p>
            </div>

            {bannerError && (
              <div
                role="alert"
                className={`rounded-xl border px-4 py-3 text-sm space-y-1 ${
                  lockedUntil
                    ? 'border-amber-300 bg-hold-bg text-hold-text'
                    : 'border-cancel-text/30 bg-cancel-bg text-cancel-text'
                }`}
              >
                <p className="font-medium">{bannerError}</p>
                {lockedUntil && (
                  <p className="text-xs">
                    Thời điểm mở khóa dự kiến: <strong>{formatDateTimeGMT7(lockedUntil)} (GMT+7)</strong>.{' '}
                    <Link to="/forgot-password" className="font-semibold underline">
                      Đặt lại mật khẩu qua email
                    </Link>
                  </p>
                )}
              </div>
            )}

            {/* Email hoặc số điện thoại */}
            <div>
              <label
                htmlFor="login-identifier"
                className="block text-xs font-semibold text-stone-800 mb-1.5"
              >
                Email hoặc số điện thoại
              </label>
              <input
                id="login-identifier"
                name="identifier"
                type="text"
                autoComplete="username"
                placeholder="Nhập email hoặc số điện thoại"
                value={identifier}
                onChange={(e) => {
                  setIdentifier(e.target.value);
                  if (fieldErrors.identifier) {
                    setFieldErrors((prev) => ({ ...prev, identifier: '' }));
                  }
                  if (bannerError) setBannerError(null);
                }}
                aria-invalid={Boolean(fieldErrors.identifier)}
                className={`w-full rounded-xl border px-4 py-3 text-sm bg-white outline-none transition-colors ${
                  fieldErrors.identifier
                    ? 'border-cancel-text focus:border-cancel-text'
                    : 'border-stone-200 focus:border-brand'
                }`}
              />
              {fieldErrors.identifier && (
                <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.identifier}</p>
              )}
            </div>

            {/* Mật khẩu */}
            <div>
              <label
                htmlFor="login-password"
                className="block text-xs font-semibold text-stone-800 mb-1.5"
              >
                Mật khẩu
              </label>
              <div className="relative">
                <input
                  id="login-password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  placeholder="Nhập mật khẩu"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    if (fieldErrors.password) {
                      setFieldErrors((prev) => ({ ...prev, password: '' }));
                    }
                    if (bannerError) setBannerError(null);
                  }}
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

            {/* Ghi nhớ đăng nhập & Quên mật khẩu */}
            <div className="flex items-center justify-between gap-4 text-xs">
              <label className="inline-flex items-center gap-2 text-stone-600 cursor-pointer">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="h-4 w-4 rounded border-stone-300 text-brand focus:ring-brand"
                />
                <span>Ghi nhớ đăng nhập</span>
              </label>
              <Link
                to="/forgot-password"
                className="font-semibold text-brand hover:underline"
              >
                Quên mật khẩu?
              </Link>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-brand px-6 py-3.5 text-sm font-semibold text-white hover:bg-brand-dark transition-colors disabled:opacity-60"
            >
              <span>{isSubmitting ? 'Đang đăng nhập...' : 'Đăng nhập'}</span>
              {!isSubmitting && <span aria-hidden="true">→</span>}
            </button>

            <p className="text-center text-xs text-stone-600 pt-1">
              Chưa có tài khoản?{' '}
              <Link to="/register" className="font-semibold text-brand hover:underline">
                Đăng ký ngay
              </Link>
            </p>

            {/* Khung thông báo bảo vệ tài khoản theo Figma 10 & 12 */}
            <div className="rounded-2xl bg-brand-soft/70 p-4 space-y-1">
              <p className="text-xs font-semibold text-brand">
                Tài khoản của bạn được bảo vệ
              </p>
              <p className="text-xs text-stone-600 leading-relaxed">
                Nhập sai mật khẩu quá 5 lần liên tiếp sẽ tạm khóa đăng nhập trong 15 phút. Bạn có
                thể đặt lại mật khẩu qua email.
              </p>
            </div>

            <p className="text-[11px] text-stone-400">
              Chỉ đăng nhập trên thiết bị và kết nối bạn tin cậy.
            </p>
          </form>
        </div>
      </div>
    </section>
  );
}
