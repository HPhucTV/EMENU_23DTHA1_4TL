"""Pydantic v2 schemas và bộ kiểm tra dữ liệu đầu vào cho chức năng Tài khoản (FR-01 — US-04)."""

from datetime import datetime
import re

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
VN_PHONE_REGEX = re.compile(r"^(0[35789][0-9]{8}|02[0-9]{9})$")


def normalize_vn_phone(raw_phone: str) -> str:
    """Chuẩn hóa SĐT Việt Nam (loại bỏ khoảng trắng/dấu gạch, đổi +84 -> 0)."""
    cleaned = re.sub(r"[\s.\-()]+", "", raw_phone.strip())
    if cleaned.startswith("+84"):
        cleaned = "0" + cleaned[3:]
    elif cleaned.startswith("84") and len(cleaned) in (11, 12):
        cleaned = "0" + cleaned[2:]
    return cleaned


class RegisterRequest(BaseModel):
    full_name: str = Field(
        description="Họ và tên khách hàng",
        examples=["Nguyễn Văn Khách"],
    )
    phone: str = Field(
        description="Số điện thoại Việt Nam (10 số di động hoặc 11 số cố định)",
        examples=["0901234567"],
    )
    email: str = Field(
        description="Địa chỉ email dùng để đăng nhập và nhận thư xác thực",
        examples=["khach@example.com"],
    )
    password: str = Field(
        description="Mật khẩu từ 8 đến 64 ký tự, gồm ít nhất 1 chữ cái và 1 chữ số",
        examples=["VuonPho2026"],
    )
    confirm_password: str | None = Field(
        default=None,
        description="Nhập lại mật khẩu để xác nhận khớp",
        examples=["VuonPho2026"],
    )
    accepted_terms: bool = Field(
        default=True,
        description="Đồng ý với Điều khoản sử dụng và Chính sách bảo mật",
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        normalized = " ".join(value.strip().split())
        if len(normalized) < 2:
            raise ValueError("Họ và tên phải có ít nhất 2 ký tự.")
        if len(normalized) > 120:
            raise ValueError("Họ và tên không được vượt quá 120 ký tự.")
        return normalized

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        normalized = normalize_vn_phone(value)
        if not normalized:
            raise ValueError("Vui lòng nhập số điện thoại.")
        if not VN_PHONE_REGEX.match(normalized):
            raise ValueError(
                "Số điện thoại không đúng định dạng Việt Nam (ví dụ: 0901234567 hoặc +84901234567)."
            )
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not normalized:
            raise ValueError("Vui lòng nhập địa chỉ email.")
        if len(normalized) > 255 or not EMAIL_REGEX.match(normalized):
            raise ValueError(
                "Địa chỉ email không hợp lệ (ví dụ: khach@example.com)."
            )
        return normalized

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Mật khẩu phải có ít nhất 8 ký tự.")
        if len(value.encode("utf-8")) > 64:
            raise ValueError("Mật khẩu không được vượt quá 64 ký tự.")
        if not re.search(r"[A-Za-zÀ-ỹ]", value) or not re.search(r"[0-9]", value):
            raise ValueError(
                "Mật khẩu phải bao gồm ít nhất 1 chữ cái và 1 chữ số."
            )
        return value

    @field_validator("accepted_terms")
    @classmethod
    def validate_terms(cls, value: bool) -> bool:
        if not value:
            raise ValueError(
                "Bạn cần đồng ý với Điều khoản sử dụng và Chính sách bảo mật của Vườn Phố."
            )
        return value

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "RegisterRequest":
        if (
            self.confirm_password is not None
            and self.password != self.confirm_password
        ):
            raise ValueError("Mật khẩu xác nhận không khớp với mật khẩu đã tạo.")
        return self


class RegisteredUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    phone: str
    role: str
    is_active: bool
    email_verified: bool
    created_at: datetime


class RegisterResponse(BaseModel):
    message: str
    verification_email_sent: bool
    user: RegisteredUserRead


class VerifyEmailRequest(BaseModel):
    token: str = Field(min_length=10, description="Token xác thực nhận từ email")


class VerifyEmailResponse(BaseModel):
    message: str
    email: str
    email_verified: bool


class ResendVerificationRequest(BaseModel):
    email: str = Field(description="Địa chỉ email đã đăng ký cần gửi lại thư xác thực")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not EMAIL_REGEX.match(normalized):
            raise ValueError("Địa chỉ email không hợp lệ.")
        return normalized
