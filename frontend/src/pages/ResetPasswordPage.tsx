import { type FormEvent, useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  confirmPasswordReset,
  extractApiError,
  validateResetToken,
} from '../services/authApi';

function validatePasswordPair(
  newPassword: string,
  confirmPassword: string,
): Record<string, string> {
  const errors: Record<string, string> = {};

  if (newPassword.length < 8) {
    errors.new_password = 'Mật khẩu phải có ít nhất 8 ký tự.';
  } else if (!/[A-Za-zÀ-ỹ]/.test(newPassword) || !/[0-9]/.test(newPassword)) {
    errors.new_password = 'Mật khẩu phải bao gồm ít nhất 1 chữ cái và 1 chữ số.';
  }

  if (!confirmPassword) {
    errors.confirm_password = 'Vui lòng nhập lại mật khẩu mới.';
  } else if (newPassword !== confirmPassword) {
    errors.confirm_password = 'Mật khẩu xác nhận không khớp với mật khẩu mới.';
  }

  return errors;
}

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token')?.trim() || '';

  const [tokenState, setTokenState] = useState<'checking' | 'valid' | 'invalid'>(
    token ? 'checking' : 'invalid',
  );
  const [tokenMessage, setTokenMessage] = useState<string>(
    token
      ? 'Đang kiểm tra tính hợp lệ của liên kết...'
      : 'Thiếu mã đặt lại mật khẩu trên đường dẫn.',
  );

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [bannerError, setBannerError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [completedMessage, setCompletedMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    let cancelled = false;

    validateResetToken(token)
      .then(() => {
        if (!cancelled) {
          setTokenState('valid');
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setTokenState('invalid');
          setTokenMessage(extractApiError(error).message);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [token]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setBannerError(null);

    const clientErrors = validatePasswordPair(newPassword, confirmPassword);
    if (Object.keys(clientErrors).length > 0) {
      setFieldErrors(clientErrors);
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await confirmPasswordReset({
        token,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });
      setCompletedMessage(response.message);
      setFieldErrors({});
    } catch (error) {
      const parsed = extractApiError(error);
      setFieldErrors(parsed.fieldErrors);
      setBannerError(parsed.message);
      if (parsed.code === 'INVALID_RESET_TOKEN') {
        setTokenState('invalid');
        setTokenMessage(parsed.message);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto px-4 sm:px-6 py-12 sm:py-16">
      <div className="rounded-3xl bg-white border border-stone-200 p-8 sm:p-10 space-y-6 shadow-sm">
        {completedMessage ? (
          <div className="space-y-5" role="status">
            <span className="inline-block rounded-full bg-brand-soft px-3.5 py-1 text-xs font-semibold text-brand">
              ✓ Đã cập nhật mật khẩu
            </span>
            <h1 className="font-serif text-3xl font-semibold text-stone-900">
              Đặt lại mật khẩu thành công
            </h1>
            <p className="text-sm text-stone-600 leading-relaxed">{completedMessage}</p>
            <div className="pt-2">
              <Link
                to="/login"
                className="inline-flex items-center gap-2 rounded-xl bg-brand px-6 py-3 text-sm font-semibold text-white hover:bg-brand-dark transition-colors"
              >
                <span>Đăng nhập ngay</span>
                <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        ) : tokenState === 'checking' ? (
          <div className="space-y-3" role="status">
            <span className="inline-block rounded-full bg-cream-subtle px-3.5 py-1 text-xs font-semibold text-stone-700">
              Đang kiểm tra
            </span>
            <h1 className="font-serif text-3xl font-semibold text-stone-900">
              Đặt lại mật khẩu Vườn Phố
            </h1>
            <p className="text-sm text-stone-600">{tokenMessage}</p>
          </div>
        ) : tokenState === 'invalid' ? (
          <div className="space-y-5" role="alert">
            <span className="inline-block rounded-full bg-cancel-bg px-3.5 py-1 text-xs font-semibold text-cancel-text">
              Liên kết không khả dụng
            </span>
            <h1 className="font-serif text-3xl font-semibold text-stone-900">
              Không thể đặt lại mật khẩu
            </h1>
            <p className="text-sm text-stone-600 leading-relaxed">{tokenMessage}</p>
            <div className="pt-2 flex flex-wrap items-center gap-3">
              <Link
                to="/forgot-password"
                className="inline-flex items-center gap-2 rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white hover:bg-brand-dark transition-colors"
              >
                <span>Yêu cầu liên kết mới</span>
                <span aria-hidden="true">→</span>
              </Link>
              <Link
                to="/login"
                className="rounded-xl border border-stone-300 px-5 py-3 text-sm font-medium text-stone-700 hover:border-brand hover:text-brand transition-colors"
              >
                Về đăng nhập
              </Link>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} noValidate className="space-y-5">
            <div>
              <span className="inline-block rounded-full bg-brand-soft px-3.5 py-1 text-xs font-semibold text-brand mb-3">
                Liên kết hợp lệ (dùng 1 lần)
              </span>
              <h1 className="font-serif text-3xl font-semibold text-stone-900">
                Tạo mật khẩu mới
              </h1>
              <p className="text-sm text-stone-600 mt-1.5">
                Mật khẩu mới tối thiểu 8 ký tự, gồm ít nhất 1 chữ cái và 1 chữ số.
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
                htmlFor="reset-new-password"
                className="block text-xs font-semibold text-stone-800 mb-1.5"
              >
                Mật khẩu mới
              </label>
              <div className="relative">
                <input
                  id="reset-new-password"
                  name="new_password"
                  type={showNewPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  placeholder="Nhập mật khẩu mới"
                  value={newPassword}
                  onChange={(e) => {
                    setNewPassword(e.target.value);
                    if (fieldErrors.new_password) {
                      setFieldErrors((prev) => ({ ...prev, new_password: '' }));
                    }
                    if (bannerError) setBannerError(null);
                  }}
                  aria-invalid={Boolean(fieldErrors.new_password)}
                  className={`w-full rounded-xl border pl-4 pr-16 py-3 text-sm bg-white outline-none transition-colors ${
                    fieldErrors.new_password
                      ? 'border-cancel-text focus:border-cancel-text'
                      : 'border-stone-200 focus:border-brand'
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowNewPassword((prev) => !prev)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-xs font-semibold text-brand hover:underline"
                >
                  {showNewPassword ? 'Ẩn' : 'Hiện'}
                </button>
              </div>
              {fieldErrors.new_password && (
                <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.new_password}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="reset-confirm-password"
                className="block text-xs font-semibold text-stone-800 mb-1.5"
              >
                Xác nhận mật khẩu mới
              </label>
              <div className="relative">
                <input
                  id="reset-confirm-password"
                  name="confirm_password"
                  type={showConfirmPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  placeholder="Nhập lại mật khẩu mới"
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value);
                    if (fieldErrors.confirm_password) {
                      setFieldErrors((prev) => ({ ...prev, confirm_password: '' }));
                    }
                    if (bannerError) setBannerError(null);
                  }}
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
                <p className="mt-1.5 text-xs text-cancel-text">{fieldErrors.confirm_password}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-brand px-6 py-3.5 text-sm font-semibold text-white hover:bg-brand-dark transition-colors disabled:opacity-60"
            >
              <span>{isSubmitting ? 'Đang lưu mật khẩu mới...' : 'Xác nhận đặt lại mật khẩu'}</span>
              {!isSubmitting && <span aria-hidden="true">→</span>}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
