import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { RoleProtectedRoute } from './components/RoleProtectedRoute';
import { AuthProvider } from './context/AuthContext';
import { CustomerLayout } from './layouts/CustomerLayout';
import { OperationsLayout } from './layouts/OperationsLayout';
import { ForgotPasswordPage } from './pages/ForgotPasswordPage';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { RegisterPage } from './pages/RegisterPage';
import { ResetPasswordPage } from './pages/ResetPasswordPage';
import { StaffManagementPage } from './pages/StaffManagementPage';
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
                  <RoleProtectedRoute allowedRoles={['customer', 'staff', 'manager']}>
                    <PlaceholderPage
                      title="Đặt một cuộc hẹn ngon"
                      storyRef="Sprint 3–4 • US-17..US-25"
                      description="Luồng chọn bàn theo khung giờ GMT+7 (giữ chỗ 10 phút chống trùng bàn) và đặt cọc Sandbox."
                    />
                  </RoleProtectedRoute>
                }
              />
              <Route
                path="/my-bookings"
                element={
                  <RoleProtectedRoute allowedRoles={['customer', 'staff', 'manager']}>
                    <PlaceholderPage
                      title="Đặt chỗ của tôi"
                      storyRef="Sprint 4 • US-26"
                      description="Quản lý cuộc hẹn sắp tới, xem mức hoàn cọc theo chính sách (100% / 50% / 0%) và hủy đặt chỗ."
                    />
                  </RoleProtectedRoute>
                }
              />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/verify-email" element={<VerifyEmailPage />} />
              <Route path="/forgot-password" element={<ForgotPasswordPage />} />
              <Route path="/reset-password" element={<ResetPasswordPage />} />
            </Route>

            <Route
              path="/ops"
              element={
                <RoleProtectedRoute allowedRoles={['staff', 'manager']}>
                  <OperationsLayout />
                </RoleProtectedRoute>
              }
            >
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
                path="staff"
                element={
                  <RoleProtectedRoute allowedRoles={['manager']}>
                    <StaffManagementPage />
                  </RoleProtectedRoute>
                }
              />
              <Route
                path="reports"
                element={
                  <RoleProtectedRoute allowedRoles={['manager']}>
                    <PlaceholderPage
                      title="Báo cáo thống kê vận hành"
                      storyRef="Sprint 6 • US-36 (Chỉ Quản lý)"
                      description="Theo dõi số đơn theo trạng thái, tỷ lệ hủy/no-show và doanh thu đặt cọc (chỉ vai trò Quản lý được phép truy cập)."
                    />
                  </RoleProtectedRoute>
                }
              />
              <Route
                path="settings"
                element={
                  <RoleProtectedRoute allowedRoles={['manager']}>
                    <PlaceholderPage
                      title="Cài đặt tham số nghiệp vụ"
                      storyRef="Sprint 3 • US-20 (Chỉ Quản lý)"
                      description="Cấu hình lượt phục vụ, thời gian giữ chỗ, mức cọc và chính sách hoàn cọc (chỉ vai trò Quản lý được phép truy cập)."
                    />
                  </RoleProtectedRoute>
                }
              />
              <Route
                path="ai"
                element={
                  <RoleProtectedRoute allowedRoles={['manager']}>
                    <PlaceholderPage
                      title="Quản trị tri thức & Giám sát Trợ lý AI"
                      storyRef="Mở rộng • US-46 (Chỉ Quản lý)"
                      description="Quản trị tri thức FAQ và theo dõi hội thoại AI đã che PII (chỉ vai trò Quản lý được phép truy cập)."
                    />
                  </RoleProtectedRoute>
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
