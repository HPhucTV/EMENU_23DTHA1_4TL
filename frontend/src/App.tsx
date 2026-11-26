import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { CustomerLayout } from './layouts/CustomerLayout';
import { OperationsLayout } from './layouts/OperationsLayout';
import { HomePage } from './pages/HomePage';
import { PlaceholderPage } from './pages/PlaceholderPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <Routes>
          <Route element={<CustomerLayout />}>
            <Route path="/" element={<HomePage />} />
            <Route
              path="/menu"
              element={
                <PlaceholderPage
                  title="Thực đơn & Đặt món trước"
                  storyRef="Sprint 2–3 • US-09, US-10, US-21"
                  description="Màn hình xem, tìm kiếm, lọc thực đơn và giỏ món đặt trước sẽ được triển khai trên khung này ở Sprint 2 và Sprint 3."
                />
              }
            />
            <Route
              path="/booking"
              element={
                <PlaceholderPage
                  title="Đặt một cuộc hẹn ngon"
                  storyRef="Sprint 3–4 • US-17..US-25"
                  description="Luồng chọn bàn theo khung giờ GMT+7 (giữ chỗ 10 phút chống trùng bàn) và đặt cọc Sandbox."
                />
              }
            />
            <Route
              path="/my-bookings"
              element={
                <PlaceholderPage
                  title="Đặt chỗ của tôi"
                  storyRef="Sprint 4 • US-26"
                  description="Quản lý cuộc hẹn sắp tới, xem mức hoàn cọc theo chính sách (100% / 50% / 0%) và hủy đặt chỗ."
                />
              }
            />
            <Route
              path="/login"
              element={
                <PlaceholderPage
                  title="Đăng nhập & Đăng ký tài khoản"
                  storyRef="Sprint 1 • US-04, US-05, US-06"
                  description="Xác thực bằng Email/SĐT, JWT phân quyền 3 vai trò (Khách hàng, Nhân viên, Quản lý) và khóa tạm 15 phút khi nhập sai quá 5 lần."
                />
              }
            />
          </Route>

          <Route path="/ops" element={<OperationsLayout />}>
            <Route
              index
              element={
                <PlaceholderPage
                  title="Không gian vận hành Vườn Phố"
                  storyRef="Sprint 1–6 • Nhân viên & Quản lý"
                  description="Khung điều hành dành cho Nhân viên và Quản lý: quản lý đặt chỗ, sơ đồ bàn trực quan, thực đơn, chuẩn bị bếp và báo cáo thống kê."
                />
              }
            />
            <Route
              path="*"
              element={
                <PlaceholderPage
                  title="Phân hệ vận hành đang chờ triển khai"
                  storyRef="Sprint 2–6"
                  description="Route đã được định tuyến sẵn trong OperationsLayout để phát triển các User Story tiếp theo không xung đột."
                />
              }
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
