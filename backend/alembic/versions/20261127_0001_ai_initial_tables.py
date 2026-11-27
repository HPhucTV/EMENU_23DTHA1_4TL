"""Khởi tạo 3 bảng AI (knowledge_docs, chat_sessions, chat_messages) trên nhánh migration ai.

Revision ID: 20261127_0001_ai
Revises:
Create Date: 2026-11-27 17:45:00+07:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20261127_0001_ai"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = ("ai",)
depends_on: str | Sequence[str] | None = ("20261126_0001_core",)


def upgrade() -> None:
    # 14. Bảng knowledge_docs (FR-13, FR-15)
    op.create_table(
        "knowledge_docs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "category",
            sa.String(length=30),
            server_default="faq",
            nullable=False,
        ),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "category IN ('faq', 'policy', 'hours', 'info')",
            name=op.f("ck_knowledge_docs_knowledge_doc_category_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["updated_by"],
            ["users.id"],
            name=op.f("fk_knowledge_docs_updated_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_knowledge_docs")),
    )
    op.create_index(
        op.f("ix_knowledge_docs_category"),
        "knowledge_docs",
        ["category"],
        unique=False,
    )
    op.create_index(
        op.f("ix_knowledge_docs_is_active"),
        "knowledge_docs",
        ["is_active"],
        unique=False,
    )
    op.create_index(
        op.f("ix_knowledge_docs_updated_by"),
        "knowledge_docs",
        ["updated_by"],
        unique=False,
    )

    # 15. Bảng chat_sessions (FR-13, FR-14)
    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("context_json", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_chat_sessions_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_chat_sessions")),
    )
    op.create_index(
        op.f("ix_chat_sessions_expires_at"),
        "chat_sessions",
        ["expires_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_chat_sessions_user_id"),
        "chat_sessions",
        ["user_id"],
        unique=False,
    )

    # 16. Bảng chat_messages (FR-13..FR-15)
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("sender", sa.String(length=20), nullable=False),
        sa.Column("masked_content", sa.Text(), nullable=False),
        sa.Column("response_meta_json", sa.JSON(), nullable=True),
        sa.Column("feedback", sa.String(length=20), nullable=True),
        sa.Column(
            "is_fallback",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "sender IN ('user', 'assistant')",
            name=op.f("ck_chat_messages_chat_message_sender_valid"),
        ),
        sa.CheckConstraint(
            "feedback IS NULL OR feedback IN ('helpful', 'unhelpful')",
            name=op.f("ck_chat_messages_chat_message_feedback_valid"),
        ),
        sa.CheckConstraint(
            "latency_ms IS NULL OR latency_ms >= 0",
            name=op.f("ck_chat_messages_chat_message_latency_non_negative"),
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["chat_sessions.id"],
            name=op.f("fk_chat_messages_session_id_chat_sessions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_chat_messages")),
    )
    op.create_index(
        op.f("ix_chat_messages_created_at"),
        "chat_messages",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_chat_messages_feedback"),
        "chat_messages",
        ["feedback"],
        unique=False,
    )
    op.create_index(
        op.f("ix_chat_messages_session_id"),
        "chat_messages",
        ["session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_chat_messages_session_id"), table_name="chat_messages")
    op.drop_index(op.f("ix_chat_messages_feedback"), table_name="chat_messages")
    op.drop_index(op.f("ix_chat_messages_created_at"), table_name="chat_messages")
    op.drop_table("chat_messages")

    op.drop_index(op.f("ix_chat_sessions_user_id"), table_name="chat_sessions")
    op.drop_index(op.f("ix_chat_sessions_expires_at"), table_name="chat_sessions")
    op.drop_table("chat_sessions")

    op.drop_index(op.f("ix_knowledge_docs_updated_by"), table_name="knowledge_docs")
    op.drop_index(op.f("ix_knowledge_docs_is_active"), table_name="knowledge_docs")
    op.drop_index(op.f("ix_knowledge_docs_category"), table_name="knowledge_docs")
    op.drop_table("knowledge_docs")
