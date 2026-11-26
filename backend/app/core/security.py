"""Các hàm bảo mật cốt lõi: băm mật khẩu một chiều (bcrypt) và token xác thực một lần."""

import hashlib
import secrets

import bcrypt


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
