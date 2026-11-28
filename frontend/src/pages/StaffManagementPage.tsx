import { type FormEvent, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { getRoleDisplayLabel } from '../context/AuthContext';
import { formatDateTimeGMT7 } from '../lib/formatters';
import { extractApiError } from '../services/authApi';
import {
  createStaffAccount,
  fetchSecurityAuditLogs,
  fetchStaffAccounts,
  lockStaffAccount,
  unlockStaffAccount,
} from '../services/usersApi';
import type { StaffAccount, StaffAccountCreatePayload } from '../types/users';

const EMAIL_PATTERN = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const VN_PHONE_PATTERN = /^(0[35789][0-9]{8}|02[0-9]{9})$/;

function formatAuditActionLabel(action: string): string {
  switch (action) {
    case 'rbac_access_denied':
      return 'Từ chối ngoài quyền (403)';
    case 'staff_account_created':
      return 'Tạo tài khoản nhân sự';
    case 'staff_account_locked':
      return 'Khóa tài khoản nhân viên';
    case 'staff_account_unlocked':
      return 'Mở khóa tài khoản nhân viên';
    case 'auth_account_locked':
      return 'Tạm khóa sai mật khẩu 5 lần';
    default:
      return action;
  }
}

export function StaffManagementPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'locked'>('all');

  const [form, setForm] = useState<StaffAccountCreatePayload>({
    full_name: '',
    phone: '',
    email: '',
    password: '',
    role: 'staff',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [feedbackBanner, setFeedbackBanner] = useState<{
    type: 'success' | 'error';
    text: string;
  } | null>(null);

  const staffQuery = useQuery({
    queryKey: ['staff-accounts', search, statusFilter],
    queryFn: () =>
      fetchStaffAccounts({
        search: search.trim() || undefined,
        status_filter: statusFilter === 'all' ? undefined : statusFilter,
      }),
  });

  const auditLogsQuery = useQuery({
    queryKey: ['security-audit-logs'],
    queryFn: () => fetchSecurityAuditLogs(15),
  });

  const invalidateStaffData = async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ['staff-accounts'] }),
      queryClient.invalidateQueries({ queryKey: ['security-audit-logs'] }),
    ]);
  };

  const createMutation = useMutation({
    mutationFn: createStaffAccount,
    onSuccess: async (res) => {
      setFeedbackBanner({ type: 'success', text: res.message });
      setFieldErrors({});
      setForm({
        full_name: '',
        phone: '',
        email: '',
        password: '',
        role: 'staff',
      });
      await invalidateStaffData();
    },
    onError: (err) => {
      const parsed = extractApiError(err);
      setFieldErrors(parsed.fieldErrors);
      setFeedbackBanner({ type: 'error', text: parsed.message });
    },
  });

  const lockMutation = useMutation({
    mutationFn: ({ userId, reason }: { userId: number; reason?: string }) =>
      lockStaffAccount(userId, reason),
    onSuccess: async (res) => {
      setFeedbackBanner({ type: 'success', text: res.message });
      await invalidateStaffData();
    },
    onError: (err) => {
      setFeedbackBanner({ type: 'error', text: extractApiError(err).message });
    },
  });

  const unlockMutation = useMutation({
    mutationFn: (userId: number) => unlockStaffAccount(userId),
    onSuccess: async (res) => {
      setFeedbackBanner({ type: 'success', text: res.message });
      await invalidateStaffData();
    },
    onError: (err) => {
      setFeedbackBanner({ type: 'error', text: extractApiError(err).message });
    },
  });

  const handleCreateSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFeedbackBanner(null);

    const errors: Record<string, string> = {};
    if (form.full_name.trim().length < 2) {
      errors.full_name = 'Họ và tên nhân viên phải có ít nhất 2 ký tự.';
    }
    const cleanPhone = form.phone.trim().replace(/[\s.\-()]+/g, '');
    if (!VN_PHONE_PATTERN.test(cleanPhone.startsWith('+84') ? `0${cleanPhone.slice(3)}` : cleanPhone)) {
      errors.phone = 'Số điện thoại không đúng định dạng Việt Nam.';
    }
    const cleanEmail = form.email.trim().toLowerCase();
    if (!EMAIL_PATTERN.test(cleanEmail)) {
      errors.email = 'Địa chỉ email không hợp lệ.';
    }
    if (
      form.password.length < 8 ||
      !/[A-Za-zÀ-ỹ]/.test(form.password) ||
      !/[0-9]/.test(form.password)
    ) {
      errors.password = 'Mật khẩu tối thiểu 8 ký tự, gồm ít nhất 1 chữ cái và 1 chữ số.';
    }

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    createMutation.mutate({
      ...form,
      full_name: form.full_name.trim(),
      email: cleanEmail,
      phone: form.phone.trim(),
    });
  };

  const handleToggleLock = (account: StaffAccount) => {
    setFeedbackBanner(null);
    if (account.is_active) {
      lockMutation.mutate({ userId: account.id });
    } else {
      unlockMutation.mutate(account.id);
    }
  };

  const staffList = staffQuery.data?.items ?? [];
  const totalCount =
    (staffQuery.data?.active_count ?? 0) + (staffQuery.data?.locked_count ?? 0);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900">
          Quản lý tài khoản nhân viên & Phân quyền
        </h1>
        <p className="text-sm text-stone-600 mt-1">
          Tạo, khóa, mở khóa tài khoản nhân viên và theo dõi nhật ký truy cập ngoài quyền (403).
        </p>
      </div>

      {/* Thẻ thống kê nhanh */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="rounded-2xl bg-white border border-stone-200/90 p-5">
          <p className="text-xs text-stone-500">Tổng nhân sự nội bộ</p>
          <p className="text-3xl font-semibold text-stone-900 mt-2">{totalCount}</p>
          <p className="text-xs text-stone-500 mt-1">Vai trò Nhân viên & Quản lý</p>
        </div>
        <div className="rounded-2xl bg-white border border-stone-200/90 p-5">
          <p className="text-xs text-stone-500">Đang hoạt động</p>
          <p className="text-3xl font-semibold text-brand mt-2">
            {staffQuery.data?.active_count ?? 0}
          </p>
          <p className="text-xs text-stone-500 mt-1">Được phép đăng nhập vận hành</p>
        </div>
        <div className="rounded-2xl bg-white border border-stone-200/90 p-5">
          <p className="text-xs text-stone-500">Đang bị khóa</p>
          <p className="text-3xl font-semibold text-cancel-text mt-2">
            {staffQuery.data?.locked_count ?? 0}
          </p>
          <p className="text-xs text-stone-500 mt-1">Đã thu hồi quyền truy cập</p>
        </div>
      </div>

      {feedbackBanner && (
        <div
          role={feedbackBanner.type === 'error' ? 'alert' : 'status'}
          className={`rounded-2xl border px-4 py-3 text-sm font-medium ${
            feedbackBanner.type === 'success'
              ? 'border-brand/20 bg-brand-soft text-brand'
              : 'border-cancel-text/30 bg-cancel-bg text-cancel-text'
          }`}
        >
          {feedbackBanner.text}
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6 items-start">
        {/* Cột trái: Danh sách nhân viên & Nhật ký RBAC */}
        <div className="xl:col-span-7 space-y-6">
          <div className="rounded-2xl bg-white border border-stone-200/90 p-6 space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <h2 className="text-lg font-semibold text-stone-900">Danh sách nhân sự</h2>
              <input
                type="search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Tìm tên, email, SĐT..."
                className="rounded-xl border border-stone-200 px-3.5 py-2 text-sm outline-none focus:border-brand sm:w-60"
              />
            </div>

            <div className="flex flex-wrap gap-2">
              {(
                [
                  { id: 'all', label: 'Tất cả' },
                  { id: 'active', label: 'Hoạt động' },
                  { id: 'locked', label: 'Đã khóa' },
                ] as const
              ).map((tab) => (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setStatusFilter(tab.id)}
                  className={`rounded-xl px-4 py-2 text-xs font-semibold transition-colors ${
                    statusFilter === tab.id
                      ? 'bg-brand text-white'
                      : 'bg-cream-subtle text-stone-700 hover:bg-stone-200/70'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-stone-200 text-[11px] uppercase tracking-wider text-stone-500">
                    <th className="py-3 pr-3">Nhân sự</th>
                    <th className="py-3 pr-3">Vai trò</th>
                    <th className="py-3 pr-3">Trạng thái</th>
                    <th className="py-3 text-right">Thao tác</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {staffQuery.isLoading ? (
                    <tr>
                      <td colSpan={4} className="py-6 text-center text-stone-500">
                        Đang tải danh sách nhân viên...
                      </td>
                    </tr>
                  ) : staffList.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="py-6 text-center text-stone-500">
                        Chưa có tài khoản phù hợp bộ lọc.
                      </td>
                    </tr>
                  ) : (
                    staffList.map((account) => (
                      <tr key={account.id}>
                        <td className="py-3.5 pr-3">
                          <p className="font-semibold text-stone-900">{account.full_name}</p>
                          <p className="text-xs text-stone-500">
                            {account.email} • {account.phone}
                          </p>
                        </td>
                        <td className="py-3.5 pr-3">
                          <span className="rounded-lg bg-cream-subtle px-2.5 py-1 text-xs font-medium text-stone-700">
                            {getRoleDisplayLabel(account.role)}
                          </span>
                        </td>
                        <td className="py-3.5 pr-3">
                          <span
                            className={`rounded-lg px-2.5 py-1 text-xs font-semibold ${
                              account.is_active
                                ? 'bg-brand-soft text-brand'
                                : 'bg-cancel-bg text-cancel-text'
                            }`}
                          >
                            {account.is_active ? 'Hoạt động' : 'Đã khóa'}
                          </span>
                        </td>
                        <td className="py-3.5 text-right">
                          {account.role === 'staff' ? (
                            <button
                              type="button"
                              onClick={() => handleToggleLock(account)}
                              disabled={lockMutation.isPending || unlockMutation.isPending}
                              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-colors ${
                                account.is_active
                                  ? 'bg-cancel-bg text-cancel-text hover:bg-red-100'
                                  : 'bg-brand text-white hover:bg-brand-dark'
                              }`}
                            >
                              {account.is_active ? 'Khóa tài khoản' : 'Mở khóa'}
                            </button>
                          ) : (
                            <span className="text-xs text-stone-400">Quản trị viên</span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Nhật ký bảo mật RBAC & tài khoản */}
          <div className="rounded-2xl bg-white border border-stone-200/90 p-6 space-y-4">
            <h2 className="text-lg font-semibold text-stone-900">
              Nhật ký phân quyền (403) & tài khoản
            </h2>
            {(auditLogsQuery.data?.items ?? []).length === 0 ? (
              <p className="text-sm text-stone-500">Chưa ghi nhận sự kiện bảo mật nào.</p>
            ) : (
              <ul className="divide-y divide-stone-100 text-xs">
                {(auditLogsQuery.data?.items ?? []).map((log) => (
                  <li key={log.id} className="py-2.5 flex items-start justify-between gap-4">
                    <div>
                      <p className="font-semibold text-stone-800">
                        {formatAuditActionLabel(log.action)}
                      </p>
                      <p className="text-stone-600 mt-0.5">{log.reason || '—'}</p>
                    </div>
                    <span className="text-stone-400 shrink-0">
                      {formatDateTimeGMT7(log.created_at)}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Cột phải: Biểu mẫu tạo tài khoản Nhân viên */}
        <div className="xl:col-span-5 rounded-2xl bg-white border border-stone-200/90 p-6 space-y-5">
          <div>
            <h2 className="text-lg font-semibold text-stone-900">Tạo tài khoản nhân viên mới</h2>
            <p className="text-xs text-stone-500 mt-1">
              Tài khoản tạo bởi Quản lý được kích hoạt sẵn để nhân viên đăng nhập vận hành ngay.
            </p>
          </div>

          <form onSubmit={handleCreateSubmit} noValidate className="space-y-4">
            <div>
              <label
                htmlFor="staff-full-name"
                className="block text-xs font-semibold text-stone-800 mb-1"
              >
                Họ và tên nhân viên *
              </label>
              <input
                id="staff-full-name"
                type="text"
                placeholder="VD: Trần Thị Lễ Tân"
                value={form.full_name}
                onChange={(e) => {
                  setForm((prev) => ({ ...prev, full_name: e.target.value }));
                  if (fieldErrors.full_name) {
                    setFieldErrors((prev) => ({ ...prev, full_name: '' }));
                  }
                }}
                className="w-full rounded-xl border border-stone-200 px-3.5 py-2.5 text-sm outline-none focus:border-brand"
              />
              {fieldErrors.full_name && (
                <p className="mt-1 text-xs text-cancel-text">{fieldErrors.full_name}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="staff-phone"
                className="block text-xs font-semibold text-stone-800 mb-1"
              >
                Số điện thoại *
              </label>
              <input
                id="staff-phone"
                type="tel"
                placeholder="0908111222"
                value={form.phone}
                onChange={(e) => {
                  setForm((prev) => ({ ...prev, phone: e.target.value }));
                  if (fieldErrors.phone) {
                    setFieldErrors((prev) => ({ ...prev, phone: '' }));
                  }
                }}
                className="w-full rounded-xl border border-stone-200 px-3.5 py-2.5 text-sm outline-none focus:border-brand"
              />
              {fieldErrors.phone && (
                <p className="mt-1 text-xs text-cancel-text">{fieldErrors.phone}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="staff-email"
                className="block text-xs font-semibold text-stone-800 mb-1"
              >
                Email đăng nhập *
              </label>
              <input
                id="staff-email"
                type="email"
                placeholder="nhanvien@vuonpho.vn"
                value={form.email}
                onChange={(e) => {
                  setForm((prev) => ({ ...prev, email: e.target.value }));
                  if (fieldErrors.email) {
                    setFieldErrors((prev) => ({ ...prev, email: '' }));
                  }
                }}
                className="w-full rounded-xl border border-stone-200 px-3.5 py-2.5 text-sm outline-none focus:border-brand"
              />
              {fieldErrors.email && (
                <p className="mt-1 text-xs text-cancel-text">{fieldErrors.email}</p>
              )}
            </div>

            <div>
              <label
                htmlFor="staff-password"
                className="block text-xs font-semibold text-stone-800 mb-1"
              >
                Mật khẩu khởi tạo *
              </label>
              <div className="relative">
                <input
                  id="staff-password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Tối thiểu 8 ký tự, gồm chữ và số"
                  value={form.password}
                  onChange={(e) => {
                    setForm((prev) => ({ ...prev, password: e.target.value }));
                    if (fieldErrors.password) {
                      setFieldErrors((prev) => ({ ...prev, password: '' }));
                    }
                  }}
                  className="w-full rounded-xl border border-stone-200 pl-3.5 pr-14 py-2.5 text-sm outline-none focus:border-brand"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-semibold text-brand"
                >
                  {showPassword ? 'Ẩn' : 'Hiện'}
                </button>
              </div>
              {fieldErrors.password && (
                <p className="mt-1 text-xs text-cancel-text">{fieldErrors.password}</p>
              )}
            </div>

            <button
              type="submit"
              disabled={createMutation.isPending}
              className="w-full rounded-xl bg-brand px-5 py-3 text-sm font-semibold text-white hover:bg-brand-dark transition-colors disabled:opacity-60"
            >
              {createMutation.isPending ? 'Đang tạo tài khoản...' : 'Tạo tài khoản nhân viên →'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
