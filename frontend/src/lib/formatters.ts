import { ENV } from '../config/env';

/**
 * Định dạng tiền tệ chuẩn VNĐ trên toàn bộ giao diện (VD: 185000 -> "185.000 ₫").
 */
export function formatVND(amount: number): string {
  const rounded = Math.round(amount);
  return `${rounded.toLocaleString('vi-VN')} ₫`;
}

/**
 * Định dạng ngày giờ chuẩn múi giờ Việt Nam GMT+7 (Asia/Ho_Chi_Minh).
 */
export function formatDateTimeGMT7(isoString: string | Date): string {
  const date = typeof isoString === 'string' ? new Date(isoString) : isoString;
  return new Intl.DateTimeFormat('vi-VN', {
    timeZone: ENV.TIMEZONE,
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(date);
}
