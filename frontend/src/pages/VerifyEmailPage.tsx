import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { extractApiError, verifyCustomerEmail } from '../services/authApi';

export function VerifyEmailPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token')?.trim() || '';

  const [status, setStatus] = useState<'loading' | 'success' | 'error'>(
    token ? 'loading' : 'error',
  );
  const [message, setMessage] = useState<string>(
    token
      ? 'Đang xác thực địa chỉ email của bạn...'
      : 'Thiếu mã xác thực email trên đường dẫn.',
  );

  useEffect(() => {
    if (!token) return;

    let cancelled = false;
    verifyCustomerEmail(token)
      .then((res) => {
        if (!cancelled) {
          setStatus('success');
          setMessage(res.message);
        }
      })
      .catch((error) => {
        if (!cancelled) {
          setStatus('error');
          setMessage(extractApiError(error).message);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [token]);

  return (
    <div className="max-w-xl mx-auto px-4 sm:px-6 py-16">
      <div className="rounded-3xl bg-white border border-stone-200 p-8 sm:p-10 space-y-5 shadow-sm">
        <span
          className={`inline-block rounded-full px-3.5 py-1 text-xs font-semibold ${
            status === 'success'
              ? 'bg-brand-soft text-brand'
              : status === 'error'
                ? 'bg-cancel-bg text-cancel-text'
                : 'bg-cream-subtle text-stone-700'
          }`}
        >
          {status === 'success'
            ? '✓ Đã xác thực email'
            : status === 'error'
              ? 'Không thể xác thực'
              : 'Đang kiểm tra'}
        </span>

        <h1 className="font-serif text-3xl font-semibold text-stone-900">
          Xác thực tài khoản Vườn Phố
        </h1>
        <p className="text-sm text-stone-600 leading-relaxed">{message}</p>

        <div className="pt-2 flex flex-wrap items-center gap-3">
          <Link
            to="/login"
            className="inline-flex items-center gap-2 rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white hover:bg-brand-dark transition-colors"
          >
            <span>Đi tới Đăng nhập</span>
            <span aria-hidden="true">→</span>
          </Link>
          {status === 'error' && (
            <Link
              to="/register"
              className="rounded-xl border border-stone-300 px-5 py-3 text-sm font-medium text-stone-700 hover:border-brand hover:text-brand transition-colors"
            >
              Đăng ký lại tài khoản
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
