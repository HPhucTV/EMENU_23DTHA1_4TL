import { useState } from 'react';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { getRoleDisplayLabel, useAuth } from '../context/AuthContext';

const NAV_ITEMS = [
  { to: '/', label: 'Trang chủ', end: true },
  { to: '/menu', label: 'Thực đơn' },
  { to: '/#khong-gian', label: 'Không gian' },
  { to: '/my-bookings', label: 'Đặt chỗ của tôi' },
];

export function CustomerLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { user, isAuthenticated, logout, isLoggingOut } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    setMobileMenuOpen(false);
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen flex flex-col bg-cream text-stone-900">
      <header className="sticky top-0 z-30 bg-cream/95 backdrop-blur border-b border-stone-200/80">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-20 flex items-center justify-between gap-4">
          <Link to="/" className="group flex flex-col">
            <span className="font-serif text-3xl font-semibold tracking-tight text-brand leading-none">
              Vườn Phố
            </span>
            <span className="text-[10px] tracking-[0.2em] uppercase text-stone-500 mt-1">
              Ẩm thực • Kết nối
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-stone-600">
            {NAV_ITEMS.map((item) =>
              item.to.startsWith('/#') ? (
                <a
                  key={item.to}
                  href={item.to}
                  className="hover:text-brand transition-colors"
                >
                  {item.label}
                </a>
              ) : (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) =>
                    isActive
                      ? 'text-brand font-semibold'
                      : 'hover:text-brand transition-colors'
                  }
                >
                  {item.label}
                </NavLink>
              ),
            )}
          </nav>

          <div className="hidden md:flex items-center gap-4">
            {isAuthenticated && user ? (
              <>
                {(user.role === 'staff' || user.role === 'manager') && (
                  <Link
                    to={user.role === 'staff' ? '/ops/reservations' : '/ops'}
                    className="rounded-lg bg-brand-soft px-3 py-1.5 text-xs font-semibold text-brand hover:bg-brand-muted transition-colors"
                  >
                    Vận hành ({getRoleDisplayLabel(user.role)})
                  </Link>
                )}
                <span className="text-sm font-medium text-stone-700">
                  {user.full_name}
                </span>
                <button
                  type="button"
                  onClick={handleLogout}
                  disabled={isLoggingOut}
                  className="text-sm font-medium text-cancel-text hover:underline disabled:opacity-60"
                >
                  {isLoggingOut ? 'Đang thoát...' : 'Đăng xuất'}
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-sm font-medium text-stone-700 hover:text-brand transition-colors"
                >
                  Đăng nhập
                </Link>
                <Link
                  to="/register"
                  className="text-sm font-medium text-brand hover:underline transition-colors"
                >
                  Đăng ký
                </Link>
              </>
            )}

            <Link
              to="/booking"
              className="inline-flex items-center gap-2 rounded-lg bg-brand px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-dark transition-colors"
            >
              <span>Đặt bàn ngay</span>
              <span aria-hidden="true">→</span>
            </Link>
          </div>

          <button
            type="button"
            onClick={() => setMobileMenuOpen((prev) => !prev)}
            className="md:hidden rounded-lg border border-stone-300 px-3 py-1.5 text-sm font-medium text-brand"
            aria-expanded={mobileMenuOpen}
          >
            Menu
          </button>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden border-t border-stone-200 bg-cream px-4 py-4 space-y-3">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.to}
                to={item.to.replace('/#khong-gian', '/')}
                onClick={() => setMobileMenuOpen(false)}
                className="block py-1.5 text-sm font-medium text-stone-700 hover:text-brand"
              >
                {item.label}
              </Link>
            ))}

            <div className="pt-2 border-t border-stone-200 space-y-2">
              {isAuthenticated && user ? (
                <div className="flex items-center justify-between gap-3">
                  <span className="text-sm font-medium text-stone-800">
                    {user.full_name} ({getRoleDisplayLabel(user.role)})
                  </span>
                  <button
                    type="button"
                    onClick={handleLogout}
                    disabled={isLoggingOut}
                    className="rounded-lg border border-cancel-text/40 px-3 py-1.5 text-xs font-semibold text-cancel-text"
                  >
                    Đăng xuất
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-3">
                  <Link
                    to="/login"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex-1 text-center rounded-lg border border-stone-300 py-2 text-sm font-medium text-stone-800"
                  >
                    Đăng nhập
                  </Link>
                  <Link
                    to="/register"
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex-1 text-center rounded-lg bg-brand py-2 text-sm font-medium text-white"
                  >
                    Đăng ký →
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="bg-brand-dark text-stone-200 mt-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <p className="font-serif text-3xl text-white">Vườn Phố</p>
            <p className="text-sm text-stone-300 mt-2">Một chốn xanh, vạn vị thân quen.</p>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-stone-400">
              Khám phá
            </p>
            <ul className="mt-3 space-y-2 text-sm text-stone-300">
              <li>
                <Link to="/menu" className="hover:text-white">
                  Thực đơn
                </Link>
              </li>
              <li>
                <Link to="/booking" className="hover:text-white">
                  Đặt bàn theo khung giờ
                </Link>
              </li>
              <li>
                <Link to="/ops" className="hover:text-white">
                  Không gian vận hành (NV/QL)
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-stone-400">
              Thông tin
            </p>
            <ul className="mt-3 space-y-2 text-sm text-stone-300">
              <li>1 cơ sở tại TP. Hồ Chí Minh</li>
              <li>Tiền tệ chuẩn: VNĐ (₫)</li>
              <li>Múi giờ chuẩn: Việt Nam (GMT+7)</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-white/10">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex flex-col sm:flex-row items-center justify-between text-xs text-stone-400 gap-2">
            <span>© 2026 Nhà hàng Ẩm thực Vườn Phố</span>
            <span>QL09-W • GMT+7 • VNĐ</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
