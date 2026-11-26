"""Tiện ích chuẩn hóa thời gian GMT+7 và định dạng tiền tệ VNĐ."""

from datetime import datetime, timedelta, timezone, tzinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def _load_vn_timezone() -> tzinfo:
    try:
        return ZoneInfo("Asia/Ho_Chi_Minh")
    except ZoneInfoNotFoundError:
        return timezone(timedelta(hours=7), name="Asia/Ho_Chi_Minh")


VN_TZ: tzinfo = _load_vn_timezone()


def now_gmt7() -> datetime:
    """Trả về thời điểm hiện tại có gắn múi giờ chuẩn Việt Nam (GMT+7)."""
    return datetime.now(VN_TZ)


def format_vnd(amount: int) -> str:
    """Định dạng số nguyên tiền tệ sang chuỗi hiển thị VNĐ (ví dụ: 185.000 ₫)."""
    return f"{amount:,}".replace(",", ".") + " ₫"
