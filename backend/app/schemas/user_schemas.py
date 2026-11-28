"""Pydantic v2 schemas cho chức năng Phân quyền & Quản lý tài khoản Nhân viên (FR-01 — US-07)."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.auth_schemas import (
    VN_PHONE_REGEX,
    normalize_and_validate_email,
    normalize_vn_phone,
    validate_password_strength,
)


class StaffAccountCreateRequest(BaseModel):
    full_name: str = Field(
        description="Họ và tên nhân viên",
        examples=["Lê Văn Phục Vụ"],
    )
    phone: str = Field(
        description="Số điện thoại Việt Nam (không trùng)",
        examples=["0908111222"],
    )
    email: str = Field(
        description="Địa chỉ email đăng nhập của nhân viên (không trùng)",
        examples=["nhanvien1@vuonpho.vn"],
    )
    password: str = Field(
        description="Mật khẩu khởi tạo (8-64 ký tự, gồm chữ cái và chữ số)",
        examples=["********"],
    )
    role: Literal["staff", "manager"] = Field(
        default="staff",
        description="Vai trò tài khoản nội bộ (mặc định: staff)",
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        normalized = " ".join(value.strip().split())
        if len(normalized) < 2:
            raise ValueError("Họ và tên nhân viên phải có ít nhất 2 ký tự.")
        if len(normalized) > 120:
            raise ValueError("Họ và tên không được vượt quá 120 ký tự.")
        return normalized

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        normalized = normalize_vn_phone(value)
        if not normalized:
            raise ValueError("Vui lòng nhập số điện thoại nhân viên.")
        if not VN_PHONE_REGEX.match(normalized):
            raise ValueError(
                "Số điện thoại không đúng định dạng Việt Nam (ví dụ: 0908111222)."
            )
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return normalize_and_validate_email(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)


class StaffAccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    phone: str
    role: str
    is_active: bool
    email_verified: bool
    failed_login_attempts: int
    locked_until: datetime | None
    created_at: datetime
    updated_at: datetime


class StaffListResponse(BaseModel):
    items: list[StaffAccountRead]
    total: int
    active_count: int
    locked_count: int


class StaffAccountActionResponse(BaseModel):
    message: str
    user: StaffAccountRead


class LockAccountRequest(BaseModel):
    reason: str | None = Field(
        default=None,
        max_length=300,
        description="Lý do khóa tài khoản (lưu vào nhật ký kiểm toán)",
    )


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor_id: int | None
    action: str
    old_value: dict[str, Any] | None
    new_value: dict[str, Any] | None
    reason: str | None
    created_at: datetime


class AuditLogListResponse(BaseModel):
    items: list[AuditLogRead]
    total: int


class OpsOverviewResponse(BaseModel):
    message: str
    role: Literal["staff", "manager"]
    allowed_modules: list[str]
