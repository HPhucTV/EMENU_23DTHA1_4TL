import { type FormEvent, useState } from 'react';
import { Link } from 'react-router-dom';
import { extractApiError, requestPasswordReset } from '../services/authApi';
import type { ForgotPasswordResponse } from '../types/auth';

const EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [emailError, setEmailError] = useState<string | null>(null);
  const [bannerError, setBannerError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [sentResult, setSentResult] = useState<ForgotPasswordResponse | null>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setEmailError(null);
    setBannerError(null);

    const normalized = email.trim().toLowerCase();
    if (!normalized) {
      setEmailError('Vui lòng nhập địa chỉ email đã đăng ký.');
      return;
    }
    if (!EMAIL_PATTERN.test(normalized)) {
      setEmailError('Địa chỉ email không đúng định dạng (ví dụ: khach@example.com).');
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await requestPasswordReset(normalized);
      setEmail(normalized);
      setSentResult(response);
    } catch (error) {
      const parsed = extractApiError(error);
      if (parsed.fieldErrors.email) {
        setEmailError(parsed.fieldErrors.email);
      } else {
        setBannerError(parsed.message);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      <div className="mb-5 lg:hidden">
        <Link
          to="/login"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-brand hover:underline"
        >
          <span aria-hidden="true">←</span>
          <span>Quay lại đăng nhập</span>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        <div className="hidden lg:flex lg:col-span-5 rounded-3xl bg-gradient-to-br from-brand via-brand to-brand-dark text-white p-10 flex-col justify-between relative overflow-hidden shadow-sm">
          <div className="relative z-10">
            <p className="text-xs uppercase tracking-[0.2em] text-amber-200/90 font-medium">
              Nhà hàng Ẩm thực Vườn Phố
            </p>
          </div>

          <div className="relative z-10 space-y-5 my-auto py-12">
            <h2 className="font-serif text-4xl xl:text-5xl font-semibold leading-[1.12]">
              An tâm khôi phục
              <br />
              tài khoản của bạn.
            </h2>
            <p className="text-sm text-stone-200 leading-relaxed max-w-sm">
              Chúng tôi gửi liên kết đặt lại mật khẩu có thời hạn ngắn và chỉ sử dụng được một lần
              qua email đã đăng ký.
            </p>

            <div className="pt-6 border-t border-white/15 space-y-2 text-xs">
              <p className="uppercase tracking-[0.16em] text-amber-200/90 font-medium">
                Liên kết có thời hạn &nbsp;/&nbsp; Dùng một lần
              </p>
              <p className="text-stone-300">Một chốn xanh, vạn vị thân quen.</p>
            </div>
          </div>

          <div
            aria-hidden="true"
            className="pointer-events-none absolute -bottom-24 -right-24 h-72 w-72 rounded-full bg-amber-300/10 blur-2xl"
          />
        </div>

        <div className="lg:col-span-7 rounded-3xl bg-white border border-stone-200/90 p-6 sm:p-10 shadow-sm flex flex-col justify-center">
          <div className="mb-6 hidden lg:block">
            <Link
              to="/login"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-brand hover:underline"
            >
              <span aria-hidden="true">←</span>
              <span>Quay lại đăng nhập</span>
            </Link>
          </div>

          {sentResult ? (
            <div className="space-y-6" role="status">
              <div className="rounded-2xl bg-brand-soft border border-brand/20 p-6 space-y-3">
                <p className="text-xs font-semibold uppercase tracking-wider text-brand">
                  ✓ Đã tiếp nhận yêu cầu
                </p>
                <h1 className="font-serif text-3xl font-semibold text-stone-900">
                  Kiểm tra hộp thư của bạn
                </h1>
                <p className="text-sm text-stone-700 leading-relaxed">{sentResult.message}</p>
                <p className="text-xs text-stone-600">
                  Liên kết có hiệu lực trong{' '}
                  <strong>{sentResult.expires_in_minutes} phút</strong> và tự động vô hiệu sau 1 lần
                  sử dụng.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                <Link
                  to="/login"
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand px-6 py-3 text-sm font-semibold text-white hover:bg-brand-dark transition-colors"
                >
                  <span>Về trang Đăng nhập</span>
                  <span aria-hidden="true">→</span>
                </Link>
                <button
                  type="button"
                  onClick={() => setSentResult(null)}
                  className="rounded-xl border border-stone-300 px-5 py-3 text-sm font-medium text-stone-700 hover:border-brand hover:text-brand transition-colors"
                >
                  Thử lại với email khác
                </button>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} noValidate className="space-y-5">
              <div>
                <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900">
                  Quên mật khẩu
                </h1>
                <p className="text-sm text-stone-600 mt-1.5">
                  Nhập địa chỉ email đã đăng ký để nhận liên kết tạo mật khẩu mới.
                </p>
              </div>

              {bannerError && (
                <div
                  role="alert"
                  className="rounded-xl border border-cancel-text/30 bg-cancel-bg px-4 py-3 text-sm text-cancel-text"
                >
                  {bannerError}
                </div>
              )}

              <div>
                <label
                  htmlFor="forgot-email"
                  className="block text-xs font-semibold text-stone-800 mb-1.5"
                >
                  Địa chỉ email
                </label>
                <input
                  id="forgot-email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="Nhập địa chỉ email của bạn"
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value);
                    if (emailError) setEmailError(null);
                    if (bannerError) setBannerError(null);
                  }}
                  aria-invalid={Boolean(emailError)}
                  className={`w-full rounded-xl border px-4 py-3 text-sm bg-white outline-none transition-colors ${
                    emailError
                      ? 'border-cancel-text focus:border-cancel-text'
                      : 'border-stone-200 focus:border-brand'
                  }`}
                />
                {emailError && <p className="mt-1.5 text-xs text-cancel-text">{emailError}</p>}
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-brand px-6 py-3.5 text-sm font-semibold text-white hover:bg-brand-dark transition-colors disabled:opacity-60"
              >
                <span>{isSubmitting ? 'Đang gửi liên kết...' : 'Gửi liên kết đặt lại mật khẩu'}</span>
                {!isSubmitting && <span aria-hidden="true">→</span>}
              </button>

              <div className="rounded-2xl bg-brand-soft/70 p-4 space-y-1">
                <p className="text-xs font-semibold text-brand">Lưu ý bảo mật</p>
                <p className="text-xs text-stone-600 leading-relaxed">
                  Liên kết đặt lại mật khẩu chỉ có hiệu lực trong 15 phút và chỉ sử dụng được một
                  lần duy nhất.
                </p>
              </div>
            </form>
          )}
        </div>
      </div>
    </section>
  );
}
