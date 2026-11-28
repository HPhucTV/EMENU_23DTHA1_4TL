import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CustomerLayout } from './layouts/CustomerLayout';
import { OperationsLayout } from './layouts/OperationsLayout';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { RegisterPage } from './pages/RegisterPage';
import { VerifyEmailPage } from './pages/VerifyEmailPage';

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
        <AuthProvider>
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
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/verify-email" element={<VerifyEmailPage />} />
              <Route
                path="/forgot-password"
                element={
                  <PlaceholderPage
                    title="Quên mật khẩu"
                    storyRef="Sprint 1 • US-06"
                    description="Chức năng gửi liên kết đặt lại mật khẩu dùng 1 lần qua email sẽ được triển khai ngay tại US-06."
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
                    storyRef="Sprint 1–6 • Quản lý & Nhân viên"
                    description="Khung điều hành dành cho Quản lý và Nhân viên: quản lý đặt chỗ, sơ đồ bàn trực quan, thực đơn, chuẩn bị bếp và báo cáo thống kê."
                  />
                }
              />
              <Route
                path="reservations"
                element={
                  <PlaceholderPage
                    title="Quản lý đặt chỗ hôm nay"
                    storyRef="Sprint 5 • US-31..US-33"
                    description="Điểm điều hướng mặc định của vai trò Nhân viên (staff): xử lý check-in, hoàn thành, đánh dấu không đến và đổi bàn."
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
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
