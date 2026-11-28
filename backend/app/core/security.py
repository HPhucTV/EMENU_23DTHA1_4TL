"""Các hàm bảo mật cốt lõi: băm mật khẩu (bcrypt), JWT có thời hạn và token một lần."""

from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib
import secrets
import uuid

import bcrypt
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import get_settings
from app.core.timezone import VN_TZ, now_gmt7


class TokenAuthenticationError(Exception):
    """Ngoại lệ khi JWT không hợp lệ, đã hết hạn hoặc đã bị thu hồi khi đăng xuất."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class AccessTokenBundle:
    access_token: str
    jti: str
    expires_at: datetime
    expires_in_seconds: int


@dataclass(frozen=True)
class DecodedAccessToken:
    user_id: int
    role: str
    jti: str
    issued_at: datetime
    expires_at: datetime


# Bộ nhớ đệm các JTI đã đăng xuất (kết hợp lưu bền vững trong reservation_audit_logs)
_REVOKED_TOKEN_JTIS: dict[str, datetime] = {}


def hash_password(plain_password: str) -> str:
    """Băm mật khẩu người dùng bằng thuật toán một chiều bcrypt (cost=12)."""
    password_bytes = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Kiểm tra mật khẩu nhập vào khớp với chuỗi băm lưu trong CSDL."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False


def hash_one_time_token(raw_token: str) -> str:
    """Băm SHA-256 cho token xác thực email / đặt lại mật khẩu trước khi lưu CSDL."""
    return hashlib.sha256(raw_token.strip().encode("utf-8")).hexdigest()


def generate_one_time_token() -> tuple[str, str]:
    """Sinh cặp (raw_token gửi qua email, token_hash lưu vào bảng password_reset_tokens)."""
    raw_token = secrets.token_urlsafe(32)
    return raw_token, hash_one_time_token(raw_token)


def _resolve_jwt_signing_key() -> bytes:
    """Đảm bảo khóa ký HS256 luôn đủ >= 32 bytes theo chuẩn RFC 7518."""
    raw_bytes = get_settings().jwt_secret_key.encode("utf-8")
    if len(raw_bytes) >= 32:
        return raw_bytes
    return hashlib.sha256(raw_bytes).digest()


def create_access_token(
    *,
    user_id: int,
    role: str,
    remember_me: bool = False,
    expires_delta: timedelta | None = None,
) -> AccessTokenBundle:
    """Phát hành JWT có thời hạn rõ ràng (chuẩn hóa dấu thời gian GMT+7)."""
    settings = get_settings()
    issued_at = now_gmt7()
    if expires_delta is not None:
        ttl = expires_delta
    elif remember_me:
        ttl = timedelta(days=settings.jwt_remember_expire_days)
    else:
        ttl = timedelta(minutes=settings.jwt_expire_minutes)

    expires_at = issued_at + ttl
    jti = uuid.uuid4().hex
    payload = {
        "sub": str(user_id),
        "role": role,
        "jti": jti,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    encoded = jwt.encode(
        payload,
        _resolve_jwt_signing_key(),
        algorithm=settings.jwt_algorithm,
    )
    return AccessTokenBundle(
        access_token=encoded,
        jti=jti,
        expires_at=expires_at,
        expires_in_seconds=max(1, int(ttl.total_seconds())),
    )


def decode_access_token(token: str) -> DecodedAccessToken:
    """Giải mã và xác thực chữ ký + hạn sử dụng của JWT."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            _resolve_jwt_signing_key(),
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "role", "jti", "iat", "exp"]},
        )
        user_id = int(payload["sub"])
        role = str(payload["role"])
        jti = str(payload["jti"])
        issued_at = datetime.fromtimestamp(float(payload["iat"]), tz=VN_TZ)
        expires_at = datetime.fromtimestamp(float(payload["exp"]), tz=VN_TZ)
    except ExpiredSignatureError as exc:
        raise TokenAuthenticationError(
            code="TOKEN_EXPIRED",
            message="Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.",
        ) from exc
    except (InvalidTokenError, KeyError, ValueError, TypeError) as exc:
        raise TokenAuthenticationError(
            code="INVALID_TOKEN",
            message="Mã phiên đăng nhập không hợp lệ.",
        ) from exc

    return DecodedAccessToken(
        user_id=user_id,
        role=role,
        jti=jti,
        issued_at=issued_at,
        expires_at=expires_at,
    )


def mark_jti_revoked_in_memory(jti: str, expires_at: datetime) -> None:
    """Đánh dấu JTI đã bị hủy phiên trong bộ nhớ và dọn các mục đã quá hạn."""
    current = now_gmt7()
    expired_keys = [
        key for key, exp in _REVOKED_TOKEN_JTIS.items() if exp <= current
    ]
    for key in expired_keys:
        _REVOKED_TOKEN_JTIS.pop(key, None)
    _REVOKED_TOKEN_JTIS[jti] = expires_at


def is_jti_revoked_in_memory(jti: str) -> bool:
    exp = _REVOKED_TOKEN_JTIS.get(jti)
    if exp is None:
        return False
    if exp <= now_gmt7():
        _REVOKED_TOKEN_JTIS.pop(jti, None)
        return False
    return True


def clear_revoked_jtis_in_memory() -> None:
    _REVOKED_TOKEN_JTIS.clear()
