import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { ENV } from '../config/env';
import { formatDateTimeGMT7, formatVND } from '../lib/formatters';
import { fetchHealthStatus, fetchRestaurantOverview } from '../services/systemApi';

export function HomePage() {
  const healthQuery = useQuery({
    queryKey: ['system-health'],
    queryFn: fetchHealthStatus,
    retry: 1,
  });

  const overviewQuery = useQuery({
    queryKey: ['restaurant-overview'],
    queryFn: fetchRestaurantOverview,
    retry: 1,
  });

  const overview = overviewQuery.data;
  const health = healthQuery.data;
  const isApiOnline = health?.status === 'ok';
  const isDbConnected = health?.database.status === 'connected';

  return (
    <div>
      {/* Hero Section theo Figma 01_trang_chu.png */}
      <section className="bg-brand text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-16 md:py-24 grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          <div className="lg:col-span-7 space-y-6">
            <p className="text-xs uppercase tracking-[0.22em] text-amber-200/90">
              Nhà hàng Ẩm thực Vườn Phố
            </p>
            <h1 className="font-serif text-4xl sm:text-6xl font-semibold leading-[1.08]">
              Một chốn xanh,
              <br />
              vạn vị thân quen.
            </h1>
            <p className="text-stone-200 text-base sm:text-lg max-w-xl leading-relaxed">
              Gác lại nhịp phố, quây quần bên món Việt. Chọn một góc yêu thích theo khung giờ
              GMT+7, để Vườn Phố chuẩn bị phần còn lại.
            </p>
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link
                to="/booking"
                className="inline-flex items-center gap-2 rounded-lg bg-white px-5 py-3 text-sm font-semibold text-brand hover:bg-cream transition-colors"
              >
                <span>Chọn bàn của bạn</span>
                <span aria-hidden="true">→</span>
              </Link>
              <Link
                to="/menu"
                className="inline-flex items-center gap-2 rounded-lg border border-white/30 px-5 py-3 text-sm font-medium text-white hover:bg-white/10 transition-colors"
              >
                Khám phá thực đơn ↗
              </Link>
            </div>
          </div>

          {/* Thẻ kiểm chứng kết nối thực tế FE ↔ FastAPI ↔ PostgreSQL cho US-01 */}
          <div className="lg:col-span-5">
            <div className="rounded-2xl bg-white/10 backdrop-blur border border-white/20 p-6 space-y-4">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs uppercase tracking-wider text-amber-200 font-semibold">
                  Trạng thái nền tảng (US-01)
                </span>
                <span
                  className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium ${
                    isApiOnline
                      ? 'bg-emerald-400/20 text-emerald-100'
                      : 'bg-amber-400/20 text-amber-100'
                  }`}
                >
                  <span
                    className={`h-2 w-2 rounded-full ${
                      isApiOnline ? 'bg-emerald-300' : 'bg-amber-300'
                    }`}
                  />
                  {healthQuery.isLoading
                    ? 'Đang kiểm tra API...'
                    : isApiOnline
                      ? 'FastAPI 200 OK'
                      : 'Chưa nối được Back-end'}
                </span>
              </div>

              <div className="space-y-2.5 text-sm text-stone-100">
                <div className="flex justify-between gap-4 border-b border-white/10 pb-2">
                  <span className="text-stone-300">Cơ sở dữ liệu:</span>
                  <span className="font-medium text-right">
                    {health
                      ? `${health.database.dialect} (${
                          isDbConnected
                            ? `Đã kết nối • ${health.database.latency_ms} ms`
                            : 'Chưa kết nối'
                        })`
                      : 'Đang tải...'}
                  </span>
                </div>
                <div className="flex justify-between gap-4 border-b border-white/10 pb-2">
                  <span className="text-stone-300">Chuẩn hệ thống:</span>
                  <span className="font-medium">
                    {health ? `${health.utc_offset} • ${health.currency}` : 'GMT+7 • VND'}
                  </span>
                </div>
                <div className="flex justify-between gap-4">
                  <span className="text-stone-300">Giờ máy chủ:</span>
                  <span className="font-medium">
                    {health ? formatDateTimeGMT7(health.timestamp) : '—'}
                  </span>
                </div>
              </div>

              {health && !isDbConnected && (
                <p className="rounded-lg bg-hold-bg px-3 py-2 text-xs text-hold-text">
                  {health.database.detail}
                </p>
              )}

              <div className="pt-1 flex items-center justify-between text-xs text-stone-300">
                <span>API mẫu: /api/v1/system/overview</span>
                <a
                  href={ENV.SWAGGER_URL}
                  target="_blank"
                  rel="noreferrer"
                  className="text-amber-200 hover:underline font-medium"
                >
                  Mở Swagger /docs ↗
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Thanh tra cứu nhanh khung giờ */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 -mt-8 relative z-10">
        <div className="rounded-2xl bg-white shadow-sm border border-stone-200/80 p-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 items-end">
          <div>
            <p className="text-xs text-stone-500">Bước khung giờ</p>
            <p className="mt-1 font-semibold text-stone-900">
              {overview ? `${overview.booking_rules.slot_step_minutes} phút / khung` : '30 phút / khung'}
            </p>
          </div>
          <div>
            <p className="text-xs text-stone-500">Lượt phục vụ</p>
            <p className="mt-1 font-semibold text-stone-900">
              {overview ? `${overview.booking_rules.dining_duration_minutes} phút` : '90 phút'}
            </p>
          </div>
          <div>
            <p className="text-xs text-stone-500">Giữ chỗ tạm thời</p>
            <p className="mt-1 font-semibold text-stone-900">
              {overview ? `${overview.booking_rules.hold_minutes} phút` : '10 phút'}
            </p>
          </div>
          <div>
            <p className="text-xs text-stone-500">Đặt cọc mặc định</p>
            <p className="mt-1 font-semibold text-stone-900">
              {overview ? `${overview.booking_rules.default_deposit_percent}% tạm tính` : '30% tạm tính'}
            </p>
          </div>
          <Link
            to="/booking"
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-brand px-4 py-3 text-sm font-medium text-white hover:bg-brand-dark transition-colors"
          >
            <span>Tìm bàn trống</span>
            <span aria-hidden="true">→</span>
          </Link>
        </div>
      </section>

      {/* Thực đơn tiêu biểu nạp trực tiếp từ API mẫu Back-end */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 pt-16">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-brand">
              Từ căn bếp Vườn Phố
            </p>
            <h2 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900 mt-1">
              Những hương vị muốn sẻ chia
            </h2>
          </div>
          <Link to="/menu" className="text-sm font-semibold text-brand hover:underline">
            Xem thực đơn →
          </Link>
        </div>

        {overviewQuery.isError && (
          <div className="mt-6 rounded-xl border border-amber-300 bg-hold-bg p-4 text-sm text-hold-text">
            Chưa tải được dữ liệu từ <code>/api/v1/system/overview</code>. Hãy chắc chắn Back-end
            FastAPI đang chạy tại cổng <code>8000</code>.
          </div>
        )}

        <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {(overview?.signature_dishes ?? []).map((dish) => (
            <article
              key={dish.code}
              className="rounded-2xl bg-white border border-stone-200/80 p-5 flex flex-col justify-between shadow-sm"
            >
              <div>
                <span className="text-[11px] font-semibold uppercase tracking-wider text-brand">
                  {dish.category}
                </span>
                <h3 className="text-lg font-semibold text-stone-900 mt-1">{dish.name}</h3>
                <p className="text-sm text-stone-600 mt-2 leading-relaxed">{dish.description}</p>
              </div>
              <div className="mt-5 pt-3 border-t border-stone-100 flex items-center justify-between">
                <span className="font-semibold text-stone-900">{formatVND(dish.price_vnd)}</span>
                <span className="rounded-md bg-brand-soft px-2.5 py-1 text-xs font-medium text-brand">
                  Đang bán
                </span>
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Không gian 3 khu vực từ API mẫu */}
      <section id="khong-gian" className="max-w-6xl mx-auto px-4 sm:px-6 pt-16">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-brand">
          Chọn một góc cho riêng mình
        </p>
        <h2 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900 mt-1">
          Mỗi cuộc hẹn, một không gian.
        </h2>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          {(overview?.areas ?? []).map((area, index) => (
            <div
              key={area.code}
              className="rounded-2xl bg-white border border-stone-200/80 p-6 space-y-2"
            >
              <span className="text-xs font-semibold text-stone-400">
                0{index + 1} • Mã {area.code}
              </span>
              <h3 className="text-xl font-semibold text-stone-900">{area.name}</h3>
              <p className="text-sm text-stone-600 leading-relaxed">{area.summary}</p>
              <p className="text-xs font-medium text-brand pt-2">{area.capacity_hint}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Banner Trợ lý AI Vườn Phố (chuẩn bị điểm gắn ChatWidget cho Sprint 5) */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 pt-16">
        <div className="rounded-2xl bg-brand p-8 sm:p-10 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <p className="text-xs uppercase tracking-[0.2em] text-amber-200">
              Trợ lý AI Vườn Phố
            </p>
            <h2 className="font-serif text-3xl font-semibold">
              Chưa biết ăn gì? Cứ hỏi mình.
            </h2>
            <p className="text-sm text-stone-200">
              Tư vấn 24/7 dựa trên thực đơn và chính sách thực tế từ PostgreSQL (tích hợp tại
              Sprint 5 – US-29, US-30).
            </p>
          </div>
          <Link
            to="/menu"
            className="rounded-lg bg-white px-5 py-3 text-sm font-semibold text-brand hover:bg-cream transition-colors shrink-0"
          >
            Xem món gợi ý →
          </Link>
        </div>
      </section>
    </div>
  );
}
