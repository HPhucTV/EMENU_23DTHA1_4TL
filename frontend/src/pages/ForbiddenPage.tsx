import { Link } from 'react-router-dom';
import { getRoleDisplayLabel, useAuth } from '../context/AuthContext';

export function ForbiddenPage() {
  const { user } = useAuth();

  const homePath =
    user?.role === 'manager'
      ? '/ops'
      : user?.role === 'staff'
        ? '/ops/reservations'
        : '/';

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-16">
      <div
        role="alert"
        className="rounded-3xl bg-white border border-stone-200 p-8 sm:p-10 space-y-5 shadow-sm"
      >
        <span className="inline-block rounded-full bg-cancel-bg px-3.5 py-1 text-xs font-semibold text-cancel-text">
          403 • Không có quyền truy cập
        </span>
        <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900">
          Chức năng ngoài phạm vi vai trò
        </h1>
        <p className="text-sm text-stone-600 leading-relaxed">
          {user
            ? `Tài khoản của bạn đang ở vai trò ${getRoleDisplayLabel(user.role)} và không được cấp quyền truy cập khu vực này.`
            : 'Bạn không có quyền truy cập chức năng này.'}
        </p>
        <div className="pt-2 flex flex-wrap items-center gap-3">
          <Link
            to={homePath}
            className="inline-flex items-center gap-2 rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white hover:bg-brand-dark transition-colors"
          >
            <span>Về không gian của bạn</span>
            <span aria-hidden="true">→</span>
          </Link>
          <Link
            to="/"
            className="rounded-xl border border-stone-300 px-5 py-3 text-sm font-medium text-stone-700 hover:border-brand hover:text-brand transition-colors"
          >
            Trang chủ
          </Link>
        </div>
      </div>
    </div>
  );
}
