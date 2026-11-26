"""Định nghĩa 13 bảng ORM Core cho hệ thống Nhà hàng Ẩm thực Vườn Phố (US-02).

Phân vùng Zero File-Overlap:
- File này do Dev Fullstack sở hữu, định nghĩa toàn bộ 13 bảng nghiệp vụ cốt lõi:
  1. users
  2. password_reset_tokens
  3. categories
  4. dishes
  5. dish_price_history
  6. areas
  7. tables
  8. reservations (kèm ràng buộc PostgreSQL EXCLUDE USING gist chống trùng bàn)
  9. reservation_items (lưu giá chốt unit_price_locked, số lượng 1..20)
  10. deposit_transactions (idempotent qua provider_txn_id unique, không lưu số thẻ)
  11. reservation_audit_logs
  12. notifications (retry <= 3)
  13. business_configs
- 3 bảng AI (`knowledge_docs`, `chat_sessions`, `chat_messages`) thuộc `ai_models.py`
  do AI Dev phụ trách độc lập.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    column,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


@compiles(ExcludeConstraint, "sqlite")
def _ignore_exclude_constraint_on_sqlite(
    _element: ExcludeConstraint, _compiler: Any, **_kw: Any
) -> str | None:
    """Cho phép Base.metadata.create_all() chạy trên SQLite trong unit test
    mà không lỗi biên dịch ExcludeConstraint của PostgreSQL."""
    return None


class User(Base):
    """Bảng 1: Tài khoản người dùng 3 vai trò (customer, staff, manager) — FR-01."""

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "role IN ('customer', 'staff', 'manager')",
            name="user_role_valid",
        ),
        CheckConstraint(
            "failed_login_attempts >= 0",
            name="failed_login_attempts_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    phone: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, default="customer", server_default="customer"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    reset_tokens: Mapped[list[PasswordResetToken]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    reservations: Mapped[list[Reservation]] = relationship(
        back_populates="user", foreign_keys="Reservation.user_id"
    )


class PasswordResetToken(Base):
    """Bảng 2: Token một lần đặt lại mật khẩu / xác thực email — FR-01 (US-04, US-06)."""

    __tablename__ = "password_reset_tokens"
    __table_args__ = (
        CheckConstraint(
            "purpose IN ('password_reset', 'email_verify')",
            name="token_purpose_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    purpose: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="password_reset",
        server_default="password_reset",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped[User] = relationship(back_populates="reset_tokens")


class Category(Base):
    """Bảng 3: Danh mục thực đơn (chỉ xóa mềm) — FR-02, FR-03."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    dishes: Mapped[list[Dish]] = relationship(back_populates="category")


class Dish(Base):
    """Bảng 4: Món ăn (giá nguyên VNĐ > 0, xóa mềm, chặn xóa cứng khi đã có đơn) — FR-02, FR-03."""

    __tablename__ = "dishes"
    __table_args__ = (
        CheckConstraint("price > 0", name="dish_price_positive"),
        CheckConstraint(
            "status IN ('available', 'out_of_stock', 'discontinued')",
            name="dish_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    code: Mapped[str | None] = mapped_column(String(30), nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="available", server_default="available"
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    category: Mapped[Category] = relationship(back_populates="dishes")
    price_history: Mapped[list[DishPriceHistory]] = relationship(
        back_populates="dish"
    )
    reservation_items: Mapped[list[ReservationItem]] = relationship(
        back_populates="dish"
    )


class DishPriceHistory(Base):
    """Bảng 5: Lịch sử thay đổi giá món ăn — FR-03 (US-12)."""

    __tablename__ = "dish_price_history"
    __table_args__ = (
        CheckConstraint("old_price > 0", name="old_price_positive"),
        CheckConstraint("new_price > 0", name="new_price_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dish_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dishes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    old_price: Mapped[int] = mapped_column(Integer, nullable=False)
    new_price: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    dish: Mapped[Dish] = relationship(back_populates="price_history")


class Area(Base):
    """Bảng 6: Khu vực bàn ăn (Sân vườn, Tầng trệt, Phòng riêng VIP...) — FR-04."""

    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str | None] = mapped_column(String(20), nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    tables: Mapped[list[DiningTable]] = relationship(back_populates="area")


class DiningTable(Base):
    """Bảng 7: Bàn ăn và tọa độ sơ đồ bàn kéo thả — FR-04 (US-13, US-14, US-23)."""

    __tablename__ = "tables"
    __table_args__ = (
        CheckConstraint("capacity >= 1", name="table_capacity_min_1"),
        CheckConstraint(
            "status IN ('active', 'inactive')",
            name="table_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    area_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("areas.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    can_combine: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    pos_x: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, server_default="0"
    )
    pos_y: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, server_default="0"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active", server_default="active"
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    area: Mapped[Area] = relationship(back_populates="tables")
    reservations: Mapped[list[Reservation]] = relationship(back_populates="table")


class Reservation(Base):
    """Bảng 8: Đơn đặt chỗ 7 trạng thái, gắn ràng buộc chống trùng bàn ở tầng CSDL — FR-05..FR-09."""

    __tablename__ = "reservations"
    __table_args__ = (
        CheckConstraint("end_at > start_at", name="reservation_time_range_valid"),
        CheckConstraint("guest_count >= 1", name="reservation_guest_count_min_1"),
        CheckConstraint(
            "status IN ('pending_deposit', 'confirmed', 'checked_in', "
            "'completed', 'cancelled', 'no_show', 'expired')",
            name="reservation_status_valid",
        ),
        CheckConstraint(
            "source IN ('web', 'chat', 'phone')",
            name="reservation_source_valid",
        ),
        CheckConstraint("total_food_amount >= 0", name="total_food_non_negative"),
        CheckConstraint(
            "deposit_required >= 0", name="deposit_required_non_negative"
        ),
        CheckConstraint("deposit_paid >= 0", name="deposit_paid_non_negative"),
        CheckConstraint("refund_amount >= 0", name="refund_amount_non_negative"),
        ExcludeConstraint(
            (column("table_id"), "="),
            (func.tstzrange(column("start_at"), column("end_at"), "[)"), "&&"),
            where=text(
                "status IN ('pending_deposit', 'confirmed', 'checked_in')"
            ),
            using="gist",
            name="ex_reservations_no_overlapping_table_slot",
        ),
        Index(
            "ix_reservations_table_start_status",
            "table_id",
            "start_at",
            "status",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True, index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    customer_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    customer_phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True, index=True
    )
    customer_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    table_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tables.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    guest_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        default="pending_deposit",
        server_default="pending_deposit",
        index=True,
    )
    hold_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancel_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    checked_in_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    source: Mapped[str] = mapped_column(
        String(20), nullable=False, default="web", server_default="web"
    )
    total_food_amount: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    deposit_required: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    deposit_paid: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    refund_amount: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped[User | None] = relationship(
        back_populates="reservations", foreign_keys=[user_id]
    )
    table: Mapped[DiningTable] = relationship(back_populates="reservations")
    items: Mapped[list[ReservationItem]] = relationship(
        back_populates="reservation", cascade="all, delete-orphan"
    )
    deposit_transactions: Mapped[list[DepositTransaction]] = relationship(
        back_populates="reservation"
    )
    audit_logs: Mapped[list[ReservationAuditLog]] = relationship(
        back_populates="reservation", cascade="all, delete-orphan"
    )
    notifications: Mapped[list[Notification]] = relationship(
        back_populates="reservation", cascade="all, delete-orphan"
    )


class ReservationItem(Base):
    """Bảng 9: Món đặt trước gắn với đơn (SL 1..20, giá chốt unit_price_locked) — FR-06, FR-11."""

    __tablename__ = "reservation_items"
    __table_args__ = (
        CheckConstraint(
            "quantity >= 1 AND quantity <= 20",
            name="item_quantity_1_to_20",
        ),
        CheckConstraint(
            "unit_price_locked > 0",
            name="unit_price_locked_positive",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reservation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("reservations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    dish_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dishes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price_locked: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_prepared: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    reservation: Mapped[Reservation] = relationship(back_populates="items")
    dish: Mapped[Dish] = relationship(back_populates="reservation_items")


class DepositTransaction(Base):
    """Bảng 10: Giao dịch đặt cọc & hoàn cọc Sandbox (HMAC + idempotent, không lưu thẻ) — FR-07, FR-09."""

    __tablename__ = "deposit_transactions"
    __table_args__ = (
        CheckConstraint("amount >= 0", name="txn_amount_non_negative"),
        CheckConstraint(
            "txn_type IN ('deposit', 'refund')",
            name="txn_type_valid",
        ),
        CheckConstraint(
            "status IN ('pending', 'success', 'failed', "
            "'need_refund', 'refunded', 'manual_refund')",
            name="txn_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reservation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("reservations.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(String(30), nullable=False)
    txn_ref: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    provider_txn_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True, unique=True
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    txn_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="deposit", server_default="deposit"
    )
    status: Mapped[str] = mapped_column(
        String(25), nullable=False, default="pending", server_default="pending"
    )
    hmac_verified: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    response_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    raw_callback_meta: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    reservation: Mapped[Reservation] = relationship(
        back_populates="deposit_transactions"
    )


class ReservationAuditLog(Base):
    """Bảng 11: Nhật ký kiểm toán thay đổi đơn đặt chỗ & sự kiện phân quyền — FR-01, FR-08."""

    __tablename__ = "reservation_audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reservation_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("reservations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    actor_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    old_value: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    new_value: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    reservation: Mapped[Reservation | None] = relationship(
        back_populates="audit_logs"
    )


class Notification(Base):
    """Bảng 12: Thông báo Email & SMS nhắc lịch (retry tối đa 3 lần) — FR-10."""

    __tablename__ = "notifications"
    __table_args__ = (
        CheckConstraint(
            "channel IN ('email', 'sms')",
            name="notification_channel_valid",
        ),
        CheckConstraint(
            "event_type IN ('deposit_confirmed', 'reservation_cancelled', "
            "'reservation_updated', 'reminder_24h', 'reminder_2h', 'refund_notice')",
            name="notification_event_valid",
        ),
        CheckConstraint(
            "status IN ('pending', 'sent', 'failed', 'skipped')",
            name="notification_status_valid",
        ),
        CheckConstraint(
            "retry_count >= 0 AND retry_count <= 3",
            name="notification_retry_max_3",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reservation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("reservations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    channel: Mapped[str] = mapped_column(String(15), nullable=False)
    recipient: Mapped[str | None] = mapped_column(String(255), nullable=True)
    event_type: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", server_default="pending"
    )
    retry_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    provider_message_id: Mapped[str | None] = mapped_column(
        String(120), nullable=True
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    reservation: Mapped[Reservation] = relationship(back_populates="notifications")


class BusinessConfig(Base):
    """Bảng 13: Tham số nghiệp vụ cấu hình động bởi Quản lý — US-20."""

    __tablename__ = "business_configs"

    key: Mapped[str] = mapped_column(String(80), primary_key=True)
    value: Mapped[Any] = mapped_column(JSON, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


CORE_TABLE_NAMES: tuple[str, ...] = (
    "users",
    "password_reset_tokens",
    "categories",
    "dishes",
    "dish_price_history",
    "areas",
    "tables",
    "reservations",
    "reservation_items",
    "deposit_transactions",
    "reservation_audit_logs",
    "notifications",
    "business_configs",
)

__all__ = [
    "Area",
    "Base",
    "BusinessConfig",
    "CORE_TABLE_NAMES",
    "Category",
    "DepositTransaction",
    "DiningTable",
    "Dish",
    "DishPriceHistory",
    "Notification",
    "PasswordResetToken",
    "Reservation",
    "ReservationAuditLog",
    "ReservationItem",
    "User",
]
