"""Định nghĩa 3 bảng ORM AI cho hệ thống Chatbot Nhà hàng Ẩm thực Vườn Phố (MC-71 / WBS 1.3.5.1).

Phân vùng Zero File-Overlap:
- File này do AI Dev sở hữu độc lập, định nghĩa 3 bảng trợ lý ảo:
  14. knowledge_docs (tri thức nhà hàng: faq, policy, hours, info)
  15. chat_sessions (phiên hội thoại UUID, lưu trữ tối đa 90 ngày)
  16. chat_messages (tin nhắn đã che PII, metadata dish_cards/booking_prefill_url, feedback)
- Không chỉnh sửa `core_models.py` (13 bảng Core do Dev Fullstack phụ trách).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
import uuid

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.timezone import now_gmt7
from app.models.core_models import User

CHAT_RETENTION_DAYS: int = 90


def default_chat_session_expiry() -> datetime:
    """Trả về thời điểm hết hạn phiên chat mặc định sau 90 ngày (GMT+7)."""
    return now_gmt7() + timedelta(days=CHAT_RETENTION_DAYS)


class KnowledgeDoc(Base):
    """Bảng 14: Kho tri thức nhà hàng phục vụ RAG & quản trị Chatbot — FR-13, FR-15."""

    __tablename__ = "knowledge_docs"
    __table_args__ = (
        CheckConstraint(
            "category IN ('faq', 'policy', 'hours', 'info')",
            name="knowledge_doc_category_valid",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="faq",
        server_default="faq",
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true"), index=True
    )
    updated_by: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
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

    # Quan hệ một chiều tới User để giữ nguyên core_models.py (Zero File-Overlap)
    updater: Mapped[User | None] = relationship("User", foreign_keys=[updated_by])


class ChatSession(Base):
    """Bảng 15: Phiên hội thoại Chatbot AI (UUID, context slot-filling, lưu tối đa 90 ngày) — FR-13, FR-14."""

    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    context_json: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True, default=dict
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
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=default_chat_session_expiry,
        index=True,
    )

    # Quan hệ một chiều tới User để giữ nguyên core_models.py (Zero File-Overlap)
    user: Mapped[User | None] = relationship("User", foreign_keys=[user_id])
    messages: Mapped[list[ChatMessage]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.id",
    )


class ChatMessage(Base):
    """Bảng 16: Nhật ký tin nhắn Chatbot đã che PII kèm metadata phản hồi & đánh giá — FR-13..FR-15."""

    __tablename__ = "chat_messages"
    __table_args__ = (
        CheckConstraint(
            "sender IN ('user', 'assistant')",
            name="chat_message_sender_valid",
        ),
        CheckConstraint(
            "feedback IS NULL OR feedback IN ('helpful', 'unhelpful')",
            name="chat_message_feedback_valid",
        ),
        CheckConstraint(
            "latency_ms IS NULL OR latency_ms >= 0",
            name="chat_message_latency_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender: Mapped[str] = mapped_column(String(20), nullable=False)
    masked_content: Mapped[str] = mapped_column(Text, nullable=False)
    response_meta_json: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, nullable=True
    )
    feedback: Mapped[str | None] = mapped_column(
        String(20), nullable=True, index=True
    )
    is_fallback: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    session: Mapped[ChatSession] = relationship(back_populates="messages")


AI_TABLE_NAMES: tuple[str, ...] = (
    "knowledge_docs",
    "chat_sessions",
    "chat_messages",
)

__all__ = [
    "AI_TABLE_NAMES",
    "Base",
    "CHAT_RETENTION_DAYS",
    "ChatMessage",
    "ChatSession",
    "KnowledgeDoc",
    "default_chat_session_expiry",
]
