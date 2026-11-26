"""Dịch vụ gửi Email (hỗ trợ Console/Test, Mailpit/SMTP và Brevo REST API kèm retry <= 3 lần)."""

from dataclasses import dataclass
from email.message import EmailMessage
import logging
import smtplib
import time

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class OutboxEmail:
    to_email: str
    to_name: str
    subject: str
    html_body: str
    text_body: str
    verification_url: str | None = None


# Hộp thư bộ nhớ phục vụ kiểm tra trên môi trường dev/test khi EMAIL_PROVIDER=console
_DEV_OUTBOX: list[OutboxEmail] = []


def get_dev_outbox() -> list[OutboxEmail]:
    return list(_DEV_OUTBOX)


def clear_dev_outbox() -> None:
    _DEV_OUTBOX.clear()


def _send_via_smtp(msg: OutboxEmail) -> None:
    settings = get_settings()
    mime = EmailMessage()
    mime["Subject"] = msg.subject
    mime["From"] = f"{settings.email_from_name} <{settings.email_from_address}>"
    mime["To"] = f"{msg.to_name} <{msg.to_email}>"
    mime.set_content(msg.text_body)
    mime.add_alternative(msg.html_body, subtype="html")

    with smtplib.SMTP(
        settings.smtp_host, settings.smtp_port, timeout=8
    ) as server:
        if settings.smtp_use_tls:
            server.starttls()
        if settings.smtp_user and settings.smtp_password:
            server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(mime)


def _send_via_brevo(msg: OutboxEmail) -> None:
    settings = get_settings()
    if not settings.brevo_api_key:
        raise RuntimeError("Thiếu BREVO_API_KEY khi EMAIL_PROVIDER=brevo.")

    response = httpx.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": settings.brevo_api_key,
            "accept": "application/json",
            "content-type": "application/json",
        },
        json={
            "sender": {
                "name": settings.email_from_name,
                "email": settings.email_from_address,
            },
            "to": [{"email": msg.to_email, "name": msg.to_name}],
            "subject": msg.subject,
            "htmlContent": msg.html_body,
            "textContent": msg.text_body,
        },
        timeout=8.0,
    )
    response.raise_for_status()


def send_email_with_retry(msg: OutboxEmail, max_retries: int = 3) -> bool:
    """Gửi email theo nhà cung cấp cấu hình, tự động thử lại tối đa 3 lần khi lỗi mạng."""
    settings = get_settings()
    provider = settings.email_provider.strip().lower()

    if provider == "console":
        _DEV_OUTBOX.append(msg)
        logger.info(
            "[EMAIL-CONSOLE] Đã gửi '%s' tới <%s>%s",
            msg.subject,
            msg.to_email,
            f" | Link: {msg.verification_url}" if msg.verification_url else "",
        )
        return True

    for attempt in range(1, max_retries + 1):
        try:
            if provider == "brevo":
                _send_via_brevo(msg)
            else:
                _send_via_smtp(msg)
            return True
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Gửi email tới %s thất bại (lần %d/%d): %s",
                msg.to_email,
                attempt,
                max_retries,
                exc,
            )
            if attempt < max_retries:
                time.sleep(0.2 * attempt)

    return False


def send_verification_email(
    *, to_email: str, full_name: str, raw_token: str
) -> bool:
    """Soạn và gửi email xác thực tài khoản mới cho khách hàng (FR-01 — US-04)."""
    settings = get_settings()
    base_url = settings.frontend_base_url.rstrip("/")
    verify_url = f"{base_url}/verify-email?token={raw_token}"
    expire_hours = settings.email_verify_expire_hours

    subject = "[Vườn Phố] Xác thực tài khoản đặt bàn của bạn"
    text_body = (
        f"Xin chào {full_name},\n\n"
        f"Cảm ơn bạn đã tạo tài khoản tại {settings.restaurant_name}.\n"
        f"Vui lòng mở liên kết dưới đây để xác thực địa chỉ email (hiệu lực {expire_hours} giờ, dùng 1 lần):\n"
        f"{verify_url}\n\n"
        "Nếu bạn không thực hiện đăng ký này, vui lòng bỏ qua email.\n"
        "— Nhà hàng Ẩm thực Vườn Phố (TP.HCM · GMT+7)"
    )
    html_body = f"""
    <div style="font-family: 'Be Vietnam Pro', Arial, sans-serif; background:#F8F7F3; padding:24px; color:#1C2420;">
      <div style="max-width:560px; margin:0 auto; background:#FFFFFF; border-radius:16px; padding:32px; border:1px solid #E5E2DC;">
        <p style="font-size:12px; letter-spacing:0.16em; text-transform:uppercase; color:#1E4332; margin:0 0 8px;">
          Nhà hàng Ẩm thực Vườn Phố
        </p>
        <h2 style="margin:0 0 16px; color:#1E4332;">Xác thực tài khoản của bạn</h2>
        <p>Xin chào <strong>{full_name}</strong>,</p>
        <p>Cảm ơn bạn đã đăng ký tài khoản tại Vườn Phố. Nhấn vào nút bên dưới để xác thực email và bắt đầu đặt bàn:</p>
        <p style="margin:24px 0;">
          <a href="{verify_url}"
             style="display:inline-block; background:#1E4332; color:#FFFFFF; text-decoration:none; padding:12px 24px; border-radius:8px; font-weight:600;">
            Xác thực địa chỉ Email →
          </a>
        </p>
        <p style="font-size:13px; color:#57534E;">
          Liên kết có hiệu lực trong <strong>{expire_hours} giờ</strong> và chỉ sử dụng <strong>1 lần</strong>.<br/>
          Hoặc sao chép đường dẫn: <a href="{verify_url}" style="color:#1E4332;">{verify_url}</a>
        </p>
      </div>
    </div>
    """.strip()

    return send_email_with_retry(
        OutboxEmail(
            to_email=to_email,
            to_name=full_name,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
            verification_url=verify_url,
        )
    )
