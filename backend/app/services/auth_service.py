"""Nghiệp vụ Tài khoản: Đăng ký, Xác thực Email, Đăng nhập & Đăng xuất (FR-01 — US-04, US-05)."""

from datetime import datetime, timedelta
import math

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    DecodedAccessToken,
    create_access_token,
    generate_one_time_token,
    hash_one_time_token,
    hash_password,
    mark_jti_revoked_in_memory,
    verify_password,
)
from app.core.timezone import VN_TZ, now_gmt7
from app.models.core_models import PasswordResetToken, ReservationAuditLog, User
from app.schemas.auth_schemas import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisteredUserRead,
    RegisterRequest,
    RegisterResponse,
    VerifyEmailResponse,
    normalize_login_identifier,
    resolve_role_redirect_path,
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


class LoginAuthenticationError(Exception):
    """Ngoại lệ khi đăng nhập sai thông tin, tài khoản bị khóa tạm 15p hoặc bị vô hiệu hóa."""

    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        locked_until: datetime | None = None,
        retry_after_seconds: int | None = None,
        remaining_attempts: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.locked_until = locked_until
        self.retry_after_seconds = retry_after_seconds
        self.remaining_attempts = remaining_attempts


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


def authenticate_user(db: Session, payload: LoginRequest) -> LoginResponse:
    """Đăng nhập bằng Email hoặc SĐT, kiểm tra khóa tạm 15 phút sau 5 lần sai và cấp JWT."""
    settings = get_settings()
    kind, normalized_identifier = normalize_login_identifier(payload.identifier)

    criterion = (
        User.email == normalized_identifier
        if kind == "email"
        else User.phone == normalized_identifier
    )
    user = db.execute(select(User).where(criterion)).scalar_one_or_none()

    if user is None:
        raise LoginAuthenticationError(
            code="INVALID_CREDENTIALS",
            message="Email/số điện thoại hoặc mật khẩu không chính xác.",
            status_code=401,
        )

    if not user.is_active:
        raise LoginAuthenticationError(
            code="ACCOUNT_INACTIVE",
            message="Tài khoản của bạn đang bị khóa bởi Quản lý nhà hàng.",
            status_code=403,
        )

    current_time = now_gmt7()
    lock_expired_reset = False

    # 1. Nếu tài khoản đang trong thời gian khóa tạm 15 phút -> chặn ngay cả khi nhập đúng mật khẩu
    if user.locked_until is not None:
        locked_until_gmt7 = _ensure_gmt7(user.locked_until)
        if locked_until_gmt7 > current_time:
            remaining_secs = max(
                1, math.ceil((locked_until_gmt7 - current_time).total_seconds())
            )
            remaining_mins = max(1, math.ceil(remaining_secs / 60))
            raise LoginAuthenticationError(
                code="ACCOUNT_LOCKED",
                message=(
                    f"Tài khoản đang tạm khóa do nhập sai mật khẩu quá số lần quy định. "
                    f"Vui lòng thử lại sau khoảng {remaining_mins} phút."
                ),
                status_code=423,
                locked_until=locked_until_gmt7,
                retry_after_seconds=remaining_secs,
            )
        # Đã hết thời gian khóa 15 phút -> đặt lại bộ đếm trước khi kiểm tra lần thử mới
        user.failed_login_attempts = 0
        user.locked_until = None
        lock_expired_reset = True

    # 2. Kiểm tra mật khẩu băm bcrypt
    if not verify_password(payload.password, user.password_hash):
        user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
        max_attempts = settings.max_failed_login_attempts
        lockout_minutes = settings.account_lockout_minutes

        if user.failed_login_attempts >= max_attempts:
            lock_until = current_time + timedelta(minutes=lockout_minutes)
            user.locked_until = lock_until
            db.add(
                ReservationAuditLog(
                    actor_id=user.id,
                    action="auth_account_locked",
                    new_value={
                        "failed_login_attempts": user.failed_login_attempts,
                        "locked_until": lock_until.isoformat(),
                    },
                    reason="Sai mật khẩu liên tiếp chạm ngưỡng khóa tạm thời",
                )
            )
            db.commit()
            raise LoginAuthenticationError(
                code="ACCOUNT_LOCKED",
                message=(
                    f"Bạn đã nhập sai mật khẩu {max_attempts} lần liên tiếp. "
                    f"Tài khoản tạm khóa đăng nhập trong {lockout_minutes} phút."
                ),
                status_code=423,
                locked_until=lock_until,
                retry_after_seconds=lockout_minutes * 60,
                remaining_attempts=0,
            )

        remaining = max_attempts - user.failed_login_attempts
        db.commit()
        raise LoginAuthenticationError(
            code="INVALID_CREDENTIALS",
            message=(
                f"Email/số điện thoại hoặc mật khẩu không chính xác. "
                f"Còn {remaining} lần thử trước khi tạm khóa {lockout_minutes} phút."
            ),
            status_code=401,
            remaining_attempts=remaining,
        )

    # 3. Đăng nhập hợp lệ -> xóa bộ đếm sai và phát hành JWT có thời hạn
    if (
        lock_expired_reset
        or user.failed_login_attempts > 0
        or user.locked_until is not None
    ):
        user.failed_login_attempts = 0
        user.locked_until = None
        db.commit()
        db.refresh(user)

    token_bundle = create_access_token(
        user_id=user.id,
        role=user.role,
        remember_me=payload.remember_me,
    )
    redirect_path = resolve_role_redirect_path(user.role)

    return LoginResponse(
        message="Đăng nhập thành công!",
        access_token=token_bundle.access_token,
        token_type="bearer",
        expires_in=token_bundle.expires_in_seconds,
        expires_at=token_bundle.expires_at,
        redirect_path=redirect_path,
        user=RegisteredUserRead.model_validate(user),
    )


def revoke_user_session(
    db: Session, user: User, token_data: DecodedAccessToken
) -> LogoutResponse:
    """Hủy hiệu lực phiên JWT hiện tại khi người dùng đăng xuất (FR-01 — US-05)."""
    mark_jti_revoked_in_memory(token_data.jti, token_data.expires_at)
    db.add(
        ReservationAuditLog(
            actor_id=user.id,
            action="auth_logout",
            new_value={"expires_at": token_data.expires_at.isoformat()},
            reason=token_data.jti,
        )
    )
    db.commit()
    return LogoutResponse(
        message="Đăng xuất thành công. Phiên làm việc đã được hủy."
    )


def build_current_user_response(
    user: User, token_data: DecodedAccessToken
) -> CurrentUserResponse:
    return CurrentUserResponse(
        user=RegisteredUserRead.model_validate(user),
        redirect_path=resolve_role_redirect_path(user.role),
        session_expires_at=token_data.expires_at,
    )
