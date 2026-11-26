"""Khởi tạo 13 bảng Core và ràng buộc chống trùng bàn PostgreSQL btree_gist (US-02).

Revision ID: 20261126_0001_core
Revises:
Create Date: 2026-11-26 15:35:00+07:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20261126_0001_core"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = ("core",)
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    dialect_name = bind.dialect.name

    # 0. Bật tiện ích btree_gist bắt buộc cho EXCLUDE USING gist trên PostgreSQL
    if dialect_name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    # 1. Bảng users (FR-01)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.String(length=20),
            server_default="customer",
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "email_verified",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "failed_login_attempts",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
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
            "role IN ('customer', 'staff', 'manager')",
            name=op.f("ck_users_user_role_valid"),
        ),
        sa.CheckConstraint(
            "failed_login_attempts >= 0",
            name=op.f("ck_users_failed_login_attempts_non_negative"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("phone", name=op.f("uq_users_phone")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_phone"), "users", ["phone"], unique=True)

    # 2. Bảng password_reset_tokens (FR-01)
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "purpose",
            sa.String(length=30),
            server_default="password_reset",
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "purpose IN ('password_reset', 'email_verify')",
            name=op.f("ck_password_reset_tokens_token_purpose_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_password_reset_tokens_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_password_reset_tokens")),
        sa.UniqueConstraint(
            "token_hash",
            name=op.f("uq_password_reset_tokens_token_hash"),
        ),
    )
    op.create_index(
        op.f("ix_password_reset_tokens_user_id"),
        "password_reset_tokens",
        ["user_id"],
        unique=False,
    )

    # 3. Bảng categories (FR-02, FR-03)
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
    )

    # 4. Bảng dishes (FR-02, FR-03)
    op.create_table(
        "dishes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="available",
            nullable=False,
        ),
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
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
        sa.CheckConstraint("price > 0", name=op.f("ck_dishes_dish_price_positive")),
        sa.CheckConstraint(
            "status IN ('available', 'out_of_stock', 'discontinued')",
            name=op.f("ck_dishes_dish_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name=op.f("fk_dishes_category_id_categories"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dishes")),
        sa.UniqueConstraint("code", name=op.f("uq_dishes_code")),
    )
    op.create_index(
        op.f("ix_dishes_category_id"), "dishes", ["category_id"], unique=False
    )
    op.create_index(op.f("ix_dishes_name"), "dishes", ["name"], unique=False)

    # 5. Bảng dish_price_history (FR-03)
    op.create_table(
        "dish_price_history",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("dish_id", sa.Integer(), nullable=False),
        sa.Column("old_price", sa.Integer(), nullable=False),
        sa.Column("new_price", sa.Integer(), nullable=False),
        sa.Column("changed_by", sa.Integer(), nullable=True),
        sa.Column(
            "changed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "old_price > 0",
            name=op.f("ck_dish_price_history_old_price_positive"),
        ),
        sa.CheckConstraint(
            "new_price > 0",
            name=op.f("ck_dish_price_history_new_price_positive"),
        ),
        sa.ForeignKeyConstraint(
            ["changed_by"],
            ["users.id"],
            name=op.f("fk_dish_price_history_changed_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["dishes.id"],
            name=op.f("fk_dish_price_history_dish_id_dishes"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dish_price_history")),
    )
    op.create_index(
        op.f("ix_dish_price_history_dish_id"),
        "dish_price_history",
        ["dish_id"],
        unique=False,
    )

    # 6. Bảng areas (FR-04)
    op.create_table(
        "areas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=20), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_areas")),
        sa.UniqueConstraint("code", name=op.f("uq_areas_code")),
        sa.UniqueConstraint("name", name=op.f("uq_areas_name")),
    )

    # 7. Bảng tables (FR-04)
    op.create_table(
        "tables",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("area_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column(
            "can_combine",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("pos_x", sa.Float(), server_default="0", nullable=False),
        sa.Column("pos_y", sa.Float(), server_default="0", nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="active",
            nullable=False,
        ),
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
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
            "capacity >= 1", name=op.f("ck_tables_table_capacity_min_1")
        ),
        sa.CheckConstraint(
            "status IN ('active', 'inactive')",
            name=op.f("ck_tables_table_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["area_id"],
            ["areas.id"],
            name=op.f("fk_tables_area_id_areas"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tables")),
        sa.UniqueConstraint("code", name=op.f("uq_tables_code")),
    )
    op.create_index(op.f("ix_tables_area_id"), "tables", ["area_id"], unique=False)

    # 8. Bảng reservations (FR-05..FR-09)
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("customer_name", sa.String(length=120), nullable=True),
        sa.Column("customer_phone", sa.String(length=20), nullable=True),
        sa.Column("customer_email", sa.String(length=255), nullable=True),
        sa.Column("table_id", sa.Integer(), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("guest_count", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=25),
            server_default="pending_deposit",
            nullable=False,
        ),
        sa.Column("hold_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("cancel_reason", sa.Text(), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("checked_in_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "source",
            sa.String(length=20),
            server_default="web",
            nullable=False,
        ),
        sa.Column(
            "total_food_amount",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "deposit_required",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "deposit_paid", sa.Integer(), server_default="0", nullable=False
        ),
        sa.Column(
            "refund_amount", sa.Integer(), server_default="0", nullable=False
        ),
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
            "end_at > start_at",
            name=op.f("ck_reservations_reservation_time_range_valid"),
        ),
        sa.CheckConstraint(
            "guest_count >= 1",
            name=op.f("ck_reservations_reservation_guest_count_min_1"),
        ),
        sa.CheckConstraint(
            "status IN ('pending_deposit', 'confirmed', 'checked_in', "
            "'completed', 'cancelled', 'no_show', 'expired')",
            name=op.f("ck_reservations_reservation_status_valid"),
        ),
        sa.CheckConstraint(
            "source IN ('web', 'chat', 'phone')",
            name=op.f("ck_reservations_reservation_source_valid"),
        ),
        sa.CheckConstraint(
            "total_food_amount >= 0",
            name=op.f("ck_reservations_total_food_non_negative"),
        ),
        sa.CheckConstraint(
            "deposit_required >= 0",
            name=op.f("ck_reservations_deposit_required_non_negative"),
        ),
        sa.CheckConstraint(
            "deposit_paid >= 0",
            name=op.f("ck_reservations_deposit_paid_non_negative"),
        ),
        sa.CheckConstraint(
            "refund_amount >= 0",
            name=op.f("ck_reservations_refund_amount_non_negative"),
        ),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["tables.id"],
            name=op.f("fk_reservations_table_id_tables"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_reservations_user_id_users"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reservations")),
        sa.UniqueConstraint("code", name=op.f("uq_reservations_code")),
    )
    op.create_index(
        op.f("ix_reservations_code"), "reservations", ["code"], unique=True
    )
    op.create_index(
        op.f("ix_reservations_customer_phone"),
        "reservations",
        ["customer_phone"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reservations_hold_expires_at"),
        "reservations",
        ["hold_expires_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reservations_start_at"),
        "reservations",
        ["start_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reservations_status"), "reservations", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_reservations_table_id"),
        "reservations",
        ["table_id"],
        unique=False,
    )
    op.create_index(
        "ix_reservations_table_start_status",
        "reservations",
        ["table_id", "start_at", "status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reservations_user_id"), "reservations", ["user_id"], unique=False
    )

    # Ràng buộc chống trùng bàn ở tầng CSDL (FR-05 — Acceptance Criteria #3 của US-02)
    if dialect_name == "postgresql":
        op.execute(
            """
            ALTER TABLE reservations
            ADD CONSTRAINT ex_reservations_no_overlapping_table_slot
            EXCLUDE USING gist (
                table_id WITH =,
                tstzrange(start_at, end_at, '[)') WITH &&
            )
            WHERE (status IN ('pending_deposit', 'confirmed', 'checked_in'))
            """
        )
    elif dialect_name == "sqlite":
        op.execute(
            """
            CREATE TRIGGER trg_reservations_no_overlap_insert
            BEFORE INSERT ON reservations
            WHEN NEW.status IN ('pending_deposit', 'confirmed', 'checked_in')
            BEGIN
                SELECT RAISE(ABORT, 'ex_reservations_no_overlapping_table_slot')
                WHERE EXISTS (
                    SELECT 1
                    FROM reservations AS existing
                    WHERE existing.table_id = NEW.table_id
                      AND existing.status IN ('pending_deposit', 'confirmed', 'checked_in')
                      AND existing.start_at < NEW.end_at
                      AND NEW.start_at < existing.end_at
                );
            END;
            """
        )
        op.execute(
            """
            CREATE TRIGGER trg_reservations_no_overlap_update
            BEFORE UPDATE OF table_id, start_at, end_at, status ON reservations
            WHEN NEW.status IN ('pending_deposit', 'confirmed', 'checked_in')
            BEGIN
                SELECT RAISE(ABORT, 'ex_reservations_no_overlapping_table_slot')
                WHERE EXISTS (
                    SELECT 1
                    FROM reservations AS existing
                    WHERE existing.id != NEW.id
                      AND existing.table_id = NEW.table_id
                      AND existing.status IN ('pending_deposit', 'confirmed', 'checked_in')
                      AND existing.start_at < NEW.end_at
                      AND NEW.start_at < existing.end_at
                );
            END;
            """
        )

    # 9. Bảng reservation_items (FR-06, FR-11)
    op.create_table(
        "reservation_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("reservation_id", sa.Integer(), nullable=False),
        sa.Column("dish_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price_locked", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column(
            "is_prepared",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
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
            "quantity >= 1 AND quantity <= 20",
            name=op.f("ck_reservation_items_item_quantity_1_to_20"),
        ),
        sa.CheckConstraint(
            "unit_price_locked > 0",
            name=op.f("ck_reservation_items_unit_price_locked_positive"),
        ),
        sa.ForeignKeyConstraint(
            ["dish_id"],
            ["dishes.id"],
            name=op.f("fk_reservation_items_dish_id_dishes"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservations.id"],
            name=op.f("fk_reservation_items_reservation_id_reservations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reservation_items")),
    )
    op.create_index(
        op.f("ix_reservation_items_dish_id"),
        "reservation_items",
        ["dish_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reservation_items_reservation_id"),
        "reservation_items",
        ["reservation_id"],
        unique=False,
    )

    # 10. Bảng deposit_transactions (FR-07, FR-09)
    op.create_table(
        "deposit_transactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("reservation_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=30), nullable=False),
        sa.Column("txn_ref", sa.String(length=64), nullable=False),
        sa.Column("provider_txn_id", sa.String(length=100), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column(
            "txn_type",
            sa.String(length=20),
            server_default="deposit",
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=25),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "hmac_verified",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("response_code", sa.String(length=32), nullable=True),
        sa.Column("raw_callback_meta", sa.JSON(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "amount >= 0",
            name=op.f("ck_deposit_transactions_txn_amount_non_negative"),
        ),
        sa.CheckConstraint(
            "txn_type IN ('deposit', 'refund')",
            name=op.f("ck_deposit_transactions_txn_type_valid"),
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'success', 'failed', "
            "'need_refund', 'refunded', 'manual_refund')",
            name=op.f("ck_deposit_transactions_txn_status_valid"),
        ),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservations.id"],
            name=op.f("fk_deposit_transactions_reservation_id_reservations"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_deposit_transactions")),
        sa.UniqueConstraint(
            "provider_txn_id",
            name=op.f("uq_deposit_transactions_provider_txn_id"),
        ),
        sa.UniqueConstraint(
            "txn_ref", name=op.f("uq_deposit_transactions_txn_ref")
        ),
    )
    op.create_index(
        op.f("ix_deposit_transactions_reservation_id"),
        "deposit_transactions",
        ["reservation_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_deposit_transactions_txn_ref"),
        "deposit_transactions",
        ["txn_ref"],
        unique=True,
    )

    # 11. Bảng reservation_audit_logs (FR-01, FR-08)
    op.create_table(
        "reservation_audit_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("reservation_id", sa.Integer(), nullable=True),
        sa.Column("actor_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=60), nullable=False),
        sa.Column("old_value", sa.JSON(), nullable=True),
        sa.Column("new_value", sa.JSON(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["users.id"],
            name=op.f("fk_reservation_audit_logs_actor_id_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservations.id"],
            name=op.f("fk_reservation_audit_logs_reservation_id_reservations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reservation_audit_logs")),
    )
    op.create_index(
        op.f("ix_reservation_audit_logs_action"),
        "reservation_audit_logs",
        ["action"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reservation_audit_logs_actor_id"),
        "reservation_audit_logs",
        ["actor_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_reservation_audit_logs_reservation_id"),
        "reservation_audit_logs",
        ["reservation_id"],
        unique=False,
    )

    # 12. Bảng notifications (FR-10)
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("reservation_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=15), nullable=False),
        sa.Column("recipient", sa.String(length=255), nullable=True),
        sa.Column("event_type", sa.String(length=40), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "retry_count", sa.Integer(), server_default="0", nullable=False
        ),
        sa.Column("provider_message_id", sa.String(length=120), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "channel IN ('email', 'sms')",
            name=op.f("ck_notifications_notification_channel_valid"),
        ),
        sa.CheckConstraint(
            "event_type IN ('deposit_confirmed', 'reservation_cancelled', "
            "'reservation_updated', 'reminder_24h', 'reminder_2h', 'refund_notice')",
            name=op.f("ck_notifications_notification_event_valid"),
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'sent', 'failed', 'skipped')",
            name=op.f("ck_notifications_notification_status_valid"),
        ),
        sa.CheckConstraint(
            "retry_count >= 0 AND retry_count <= 3",
            name=op.f("ck_notifications_notification_retry_max_3"),
        ),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservations.id"],
            name=op.f("fk_notifications_reservation_id_reservations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notifications")),
    )
    op.create_index(
        op.f("ix_notifications_reservation_id"),
        "notifications",
        ["reservation_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notifications_scheduled_at"),
        "notifications",
        ["scheduled_at"],
        unique=False,
    )

    # 13. Bảng business_configs (US-20)
    op.create_table(
        "business_configs",
        sa.Column("key", sa.String(length=80), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["updated_by"],
            ["users.id"],
            name=op.f("fk_business_configs_updated_by_users"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("key", name=op.f("pk_business_configs")),
    )


def downgrade() -> None:
    bind = op.get_bind()
    dialect_name = bind.dialect.name

    op.drop_table("business_configs")
    op.drop_index(
        op.f("ix_notifications_scheduled_at"), table_name="notifications"
    )
    op.drop_index(
        op.f("ix_notifications_reservation_id"), table_name="notifications"
    )
    op.drop_table("notifications")

    op.drop_index(
        op.f("ix_reservation_audit_logs_reservation_id"),
        table_name="reservation_audit_logs",
    )
    op.drop_index(
        op.f("ix_reservation_audit_logs_actor_id"),
        table_name="reservation_audit_logs",
    )
    op.drop_index(
        op.f("ix_reservation_audit_logs_action"),
        table_name="reservation_audit_logs",
    )
    op.drop_table("reservation_audit_logs")

    op.drop_index(
        op.f("ix_deposit_transactions_txn_ref"),
        table_name="deposit_transactions",
    )
    op.drop_index(
        op.f("ix_deposit_transactions_reservation_id"),
        table_name="deposit_transactions",
    )
    op.drop_table("deposit_transactions")

    op.drop_index(
        op.f("ix_reservation_items_reservation_id"),
        table_name="reservation_items",
    )
    op.drop_index(
        op.f("ix_reservation_items_dish_id"),
        table_name="reservation_items",
    )
    op.drop_table("reservation_items")

    if dialect_name == "postgresql":
        op.execute(
            "ALTER TABLE reservations "
            "DROP CONSTRAINT IF EXISTS ex_reservations_no_overlapping_table_slot"
        )
    elif dialect_name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS trg_reservations_no_overlap_update")
        op.execute("DROP TRIGGER IF EXISTS trg_reservations_no_overlap_insert")

    op.drop_index(op.f("ix_reservations_user_id"), table_name="reservations")
    op.drop_index(
        "ix_reservations_table_start_status", table_name="reservations"
    )
    op.drop_index(op.f("ix_reservations_table_id"), table_name="reservations")
    op.drop_index(op.f("ix_reservations_status"), table_name="reservations")
    op.drop_index(op.f("ix_reservations_start_at"), table_name="reservations")
    op.drop_index(
        op.f("ix_reservations_hold_expires_at"), table_name="reservations"
    )
    op.drop_index(
        op.f("ix_reservations_customer_phone"), table_name="reservations"
    )
    op.drop_index(op.f("ix_reservations_code"), table_name="reservations")
    op.drop_table("reservations")

    op.drop_index(op.f("ix_tables_area_id"), table_name="tables")
    op.drop_table("tables")

    op.drop_table("areas")

    op.drop_index(
        op.f("ix_dish_price_history_dish_id"),
        table_name="dish_price_history",
    )
    op.drop_table("dish_price_history")

    op.drop_index(op.f("ix_dishes_name"), table_name="dishes")
    op.drop_index(op.f("ix_dishes_category_id"), table_name="dishes")
    op.drop_table("dishes")

    op.drop_table("categories")

    op.drop_index(
        op.f("ix_password_reset_tokens_user_id"),
        table_name="password_reset_tokens",
    )
    op.drop_table("password_reset_tokens")

    op.drop_index(op.f("ix_users_phone"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
