"""Nghiệp vụ Đăng ký tài khoản & Xác thực Email khách hàng (FR-01 — US-04)."""

from datetime import datetime, timedelta

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    generate_one_time_token,
    hash_one_time_token,
    hash_password,
)
from app.core.timezone import VN_TZ, now_gmt7
from app.models.core_models import PasswordResetToken, User
from app.schemas.auth_schemas import (
    RegisteredUserRead,
    RegisterRequest,
    RegisterResponse,
    VerifyEmailResponse,
)
from app.services.email_service import send_verification_email


class DuplicateAccountError(Exception):
    """Ngoại lệ khi Email hoặc SĐT đăng ký bị trùng với tài khoản đã tồn tại."""

    def __init__(self, message: str, field_errors: dict[str, str]) -> None:
        super().__init__(message)
        self.message = message
        self.field_errors = field_errors


class VerificationTokenError(Exception):
    """Ngoại lệ khi token xác thực email không hợp lệ, đã dùng hoặc hết hạn."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _ensure_gmt7(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=VN_TZ)
    return dt.astimezone(VN_TZ)


def register_customer(db: Session, payload: RegisterRequest) -> RegisterResponse:
    """Tạo tài khoản customer mới, lưu mật khẩu băm bcrypt và gửi email xác thực."""
    existing_users = (
        db.execute(
            select(User).where(
                or_(User.email == payload.email, User.phone == payload.phone)
            )
        )
        .scalars()
        .all()
    )

    if existing_users:
        field_errors: dict[str, str] = {}
        if any(u.email == payload.email for u in existing_users):
            field_errors["email"] = (
                "Email này đã được đăng ký. Vui lòng đăng nhập hoặc dùng chức năng Quên mật khẩu."
            )
        if any(u.phone == payload.phone for u in existing_users):
            field_errors["phone"] = (
                "Số điện thoại này đã được sử dụng cho một tài khoản khác."
            )
        summary_msg = next(iter(field_errors.values()))
        raise DuplicateAccountError(message=summary_msg, field_errors=field_errors)

    settings = get_settings()
    raw_token, token_hash = generate_one_time_token()
    expires_at = now_gmt7() + timedelta(hours=settings.email_verify_expire_hours)

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role="customer",
        is_active=True,
        email_verified=False,
        failed_login_attempts=0,
    )
    db.add(new_user)

    try:
        db.flush()
        verification_token = PasswordResetToken(
            user_id=new_user.id,
            token_hash=token_hash,
            purpose="email_verify",
            expires_at=expires_at,
        )
        db.add(verification_token)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateAccountError(
            message="Email hoặc số điện thoại vừa được đăng ký. Vui lòng kiểm tra lại hoặc đăng nhập.",
            field_errors={
                "email": "Email hoặc số điện thoại có thể đã tồn tại.",
            },
        ) from exc

    db.refresh(new_user)

    email_sent = send_verification_email(
        to_email=new_user.email,
        full_name=new_user.full_name,
        raw_token=raw_token,
    )

    return RegisterResponse(
        message=(
            "Đăng ký tài khoản thành công! Vui lòng kiểm tra hộp thư email để xác thực tài khoản."
            if email_sent
            else "Đăng ký tài khoản thành công, nhưng gửi email xác thực tạm thời gián đoạn. Bạn có thể bấm gửi lại sau."
        ),
        verification_email_sent=email_sent,
        user=RegisteredUserRead.model_validate(new_user),
    )


def verify_customer_email(db: Session, raw_token: str) -> VerifyEmailResponse:
    """Xác thực địa chỉ email bằng token một lần (FR-01 — US-04)."""
    token_hash = hash_one_time_token(raw_token)
    token_record = db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.purpose == "email_verify",
        )
    ).scalar_one_or_none()

    if token_record is None:
        raise VerificationTokenError(
            "Liên kết xác thực không hợp lệ hoặc không tồn tại."
        )

    if token_record.used_at is not None:
        raise VerificationTokenError(
            "Liên kết xác thực này đã được sử dụng trước đó."
        )

    current_time = now_gmt7()
    if _ensure_gmt7(token_record.expires_at) <= current_time:
        raise VerificationTokenError(
            "Liên kết xác thực đã hết hạn. Vui lòng yêu cầu gửi lại email xác thực mới."
        )

    user = db.get(User, token_record.user_id)
    if user is None:
        raise VerificationTokenError("Không tìm thấy tài khoản tương ứng.", 404)

    token_record.used_at = current_time
    user.email_verified = True
    db.commit()

    return VerifyEmailResponse(
        message="Xác thực email thành công! Bạn có thể đăng nhập và đặt bàn ngay.",
        email=user.email,
        email_verified=True,
    )


def resend_verification_email(db: Session, email: str) -> VerifyEmailResponse:
    """Cấp mới token xác thực và gửi lại email khi khách chưa nhận được thư."""
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if user is None:
        raise VerificationTokenError(
            "Không tìm thấy tài khoản gắn với địa chỉ email này.", status_code=404
        )

    if user.email_verified:
        return VerifyEmailResponse(
            message="Tài khoản này đã được xác thực trước đó. Bạn có thể đăng nhập ngay.",
            email=user.email,
            email_verified=True,
        )

    current_time = now_gmt7()
    unused_tokens = (
        db.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.purpose == "email_verify",
                PasswordResetToken.used_at.is_(None),
            )
        )
        .scalars()
        .all()
    )
    for old_token in unused_tokens:
        old_token.used_at = current_time

    settings = get_settings()
    raw_token, token_hash = generate_one_time_token()
    db.add(
        PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            purpose="email_verify",
            expires_at=current_time
            + timedelta(hours=settings.email_verify_expire_hours),
        )
    )
    db.commit()

    send_verification_email(
        to_email=user.email,
        full_name=user.full_name,
        raw_token=raw_token,
    )

    return VerifyEmailResponse(
        message="Đã gửi lại email xác thực mới. Vui lòng kiểm tra hộp thư của bạn.",
        email=user.email,
        email_verified=False,
    )
