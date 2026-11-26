import { Link, NavLink, Outlet } from 'react-router-dom';
import { formatDateTimeGMT7 } from '../lib/formatters';

const SIDEBAR_LINKS = [
  { to: '/ops', label: 'Tổng quan', end: true },
  { to: '/ops/reservations', label: 'Đặt chỗ' },
  { to: '/ops/tables', label: 'Sơ đồ bàn' },
  { to: '/ops/menu', label: 'Thực đơn' },
  { to: '/ops/kitchen', label: 'Chuẩn bị bếp' },
  { to: '/ops/reports', label: 'Báo cáo' },
  { to: '/ops/ai', label: 'Trợ lý AI' },
  { to: '/ops/settings', label: 'Cài đặt' },
];

export function OperationsLayout() {
  return (
    <div className="min-h-screen flex bg-cream text-stone-900">
      <aside className="w-64 shrink-0 bg-brand text-stone-100 flex flex-col justify-between p-6">
        <div>
          <Link to="/" className="block">
            <p className="font-serif text-3xl text-white">Vườn Phố</p>
            <p className="text-[11px] uppercase tracking-[0.18em] text-amber-200/80 mt-1">
              Không gian vận hành
            </p>
          </Link>

          <nav className="mt-8 space-y-1.5">
            {SIDEBAR_LINKS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `block rounded-lg px-3.5 py-2.5 text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-white/15 text-white'
                      : 'text-stone-300 hover:bg-white/10 hover:text-white'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="pt-6 border-t border-white/15 text-xs text-stone-300 space-y-2">
          <p className="font-medium text-white">Nhà hàng Vườn Phố</p>
          <p>1 cơ sở • TP. Hồ Chí Minh</p>
          <Link to="/" className="inline-block text-amber-200 hover:underline pt-1">
            ← Về giao diện khách hàng
          </Link>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-16 bg-white/80 border-b border-stone-200 px-8 flex items-center justify-between text-sm">
          <span className="text-stone-500">Vận hành / Khung dự án US-01</span>
          <span className="font-medium text-stone-700">
            {formatDateTimeGMT7(new Date())} (GMT+7)
          </span>
        </header>
        <main className="p-8 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
