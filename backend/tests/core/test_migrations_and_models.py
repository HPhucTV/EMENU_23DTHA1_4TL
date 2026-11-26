"""Kiểm thử tự động cho US-02 (MC-13): ERD, Alembic Migration trên CSDL trống và ràng buộc chống trùng bàn."""

from datetime import datetime
from io import StringIO
from pathlib import Path

from alembic import command
from alembic.config import Config
import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import build_engine
from app.core.timezone import VN_TZ
from app.models.core_models import (
    CORE_TABLE_NAMES,
    Area,
    Category,
    DepositTransaction,
    DiningTable,
    Dish,
    Notification,
    Reservation,
    ReservationItem,
    User,
)

BACKEND_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_DIR.parent


def _make_alembic_config(database_url: str) -> Config:
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", database_url)
    return cfg


def test_erd_document_saved_in_repository() -> None:
    erd_path = REPO_ROOT / "docs" / "ERD.md"
    assert erd_path.is_file(), "Thiếu tài liệu docs/ERD.md trong repository"

    content = erd_path.read_text(encoding="utf-8")
    assert "erDiagram" in content
    assert "ex_reservations_no_overlapping_table_slot" in content
    assert "btree_gist" in content
    for table_name in CORE_TABLE_NAMES:
        assert table_name in content


def test_alembic_creates_all_core_tables_on_empty_db_and_downgrades(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "empty_emenu.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"
    cfg = _make_alembic_config(db_url)

    # 1. Nâng cấp trên CSDL trống hoàn toàn
    command.upgrade(cfg, "heads")

    engine = build_engine(db_url)
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    for expected_table in CORE_TABLE_NAMES:
        assert (
            expected_table in existing_tables
        ), f"Thiếu bảng {expected_table} sau khi chạy migration"
    assert "alembic_version" in existing_tables
    engine.dispose()

    # 2. Hạ cấp về base (CSDL rỗng trở lại) và nâng cấp lại lần nữa
    command.downgrade(cfg, "base")
    engine_after_down = build_engine(db_url)
    remaining_tables = set(inspect(engine_after_down).get_table_names()) - {
        "alembic_version"
    }
    assert remaining_tables == set()
    engine_after_down.dispose()

    command.upgrade(cfg, "heads")
    engine_reup = build_engine(db_url)
    assert set(CORE_TABLE_NAMES).issubset(
        set(inspect(engine_reup).get_table_names())
    )
    engine_reup.dispose()


def test_postgresql_migration_sql_includes_btree_gist_and_exclude_constraint() -> None:
    sql_buffer = StringIO()
    cfg = _make_alembic_config(
        "postgresql+psycopg://emenu_user@localhost:5432/emenu_db"
    )
    cfg.output_buffer = sql_buffer

    command.upgrade(cfg, "heads", sql=True)
    generated_sql = sql_buffer.getvalue()

    assert "CREATE EXTENSION IF NOT EXISTS btree_gist" in generated_sql
    assert "ex_reservations_no_overlapping_table_slot" in generated_sql
    assert "EXCLUDE USING gist" in generated_sql
    assert "tstzrange(start_at, end_at, '[)') WITH &&" in generated_sql
    assert (
        "WHERE (status IN ('pending_deposit', 'confirmed', 'checked_in'))"
        in generated_sql
    )
    assert "TIMESTAMP WITH TIME ZONE" in generated_sql


def test_database_constraint_blocks_overlapping_table_reservations(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "overlap_check.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"
    command.upgrade(_make_alembic_config(db_url), "heads")

    engine = build_engine(db_url)
    with Session(engine) as session:
        customer = User(
            full_name="Nguyễn Văn Khách",
            email="khach1@example.com",
            phone="0901234567",
            password_hash="hashed_pw",
            role="customer",
        )
        garden = Area(code="SV", name="Sân vườn")
        session.add_all([customer, garden])
        session.flush()

        table_sv04 = DiningTable(
            area_id=garden.id,
            code="SV-04",
            capacity=4,
            pos_x=120.0,
            pos_y=80.0,
        )
        session.add(table_sv04)
        session.flush()

        # Đơn 1 giữ bàn SV-04 từ 19:00 đến 20:30 GMT+7 (pending_deposit)
        first_booking = Reservation(
            code="VP-261201-001",
            user_id=customer.id,
            table_id=table_sv04.id,
            start_at=datetime(2026, 12, 1, 19, 0, tzinfo=VN_TZ),
            end_at=datetime(2026, 12, 1, 20, 30, tzinfo=VN_TZ),
            guest_count=4,
            status="pending_deposit",
        )
        session.add(first_booking)
        session.commit()

        # Đơn 2 chồng lấn khung giờ (19:30 -> 21:00) trên cùng bàn SV-04 -> CSDL chặn ngay!
        overlapping_booking = Reservation(
            code="VP-261201-002",
            user_id=customer.id,
            table_id=table_sv04.id,
            start_at=datetime(2026, 12, 1, 19, 30, tzinfo=VN_TZ),
            end_at=datetime(2026, 12, 1, 21, 0, tzinfo=VN_TZ),
            guest_count=4,
            status="confirmed",
        )
        session.add(overlapping_booking)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

        # Đơn 3 đặt nối tiếp đúng 20:30 -> 22:00 (khoảng nửa mở [start_at, end_at)) -> Hợp lệ!
        adjacent_booking = Reservation(
            code="VP-261201-003",
            user_id=customer.id,
            table_id=table_sv04.id,
            start_at=datetime(2026, 12, 1, 20, 30, tzinfo=VN_TZ),
            end_at=datetime(2026, 12, 1, 22, 0, tzinfo=VN_TZ),
            guest_count=2,
            status="confirmed",
        )
        session.add(adjacent_booking)
        session.commit()

        # Khi đơn 1 hết hạn giữ chỗ 10 phút ('expired') -> Khung 19:00-20:30 được giải phóng!
        refreshed_first = session.get(Reservation, first_booking.id)
        assert refreshed_first is not None
        refreshed_first.status = "expired"
        session.commit()

        rebooked_slot = Reservation(
            code="VP-261201-004",
            user_id=customer.id,
            table_id=table_sv04.id,
            start_at=datetime(2026, 12, 1, 19, 0, tzinfo=VN_TZ),
            end_at=datetime(2026, 12, 1, 20, 30, tzinfo=VN_TZ),
            guest_count=4,
            status="confirmed",
        )
        session.add(rebooked_slot)
        session.commit()

    engine.dispose()


def test_restrict_delete_locked_price_and_idempotent_deposit_constraints(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "integrity_rules.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"
    command.upgrade(_make_alembic_config(db_url), "heads")

    engine = build_engine(db_url)
    with Session(engine) as session:
        category = Category(name="Món chính", sort_order=1)
        area = Area(code="TT", name="Tầng trệt")
        session.add_all([category, area])
        session.flush()

        dish = Dish(
            category_id=category.id,
            code="VP-M01",
            name="Bò cuốn lá lốt",
            price=185_000,
            tags=["đặc sản"],
        )
        table = DiningTable(area_id=area.id, code="T-01", capacity=4)
        session.add_all([dish, table])
        session.flush()

        reservation = Reservation(
            code="VP-261202-001",
            table_id=table.id,
            start_at=datetime(2026, 12, 2, 18, 0, tzinfo=VN_TZ),
            end_at=datetime(2026, 12, 2, 19, 30, tzinfo=VN_TZ),
            guest_count=4,
            status="confirmed",
            total_food_amount=370_000,
            deposit_required=111_000,
        )
        session.add(reservation)
        session.flush()

        item = ReservationItem(
            reservation_id=reservation.id,
            dish_id=dish.id,
            quantity=2,
            unit_price_locked=185_000,
        )
        txn = DepositTransaction(
            reservation_id=reservation.id,
            provider="vnpay",
            txn_ref="VNP-261202-001",
            provider_txn_id="14500991",
            amount=111_000,
            status="success",
            hmac_verified=True,
        )
        session.add_all([item, txn])
        session.commit()

        # 1. Cấm xóa cứng món ăn đã có đơn (ON DELETE RESTRICT)
        session.delete(dish)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

        # 2. Cấm ghi trùng provider_txn_id khi cổng thanh toán gọi lại webhook (Idempotent)
        duplicate_webhook_txn = DepositTransaction(
            reservation_id=reservation.id,
            provider="vnpay",
            txn_ref="VNP-261202-002",
            provider_txn_id="14500991",
            amount=111_000,
            status="success",
        )
        session.add(duplicate_webhook_txn)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

        # 3. Cấm vượt giới hạn retry_count > 3 trên bảng notifications
        invalid_notification = Notification(
            reservation_id=reservation.id,
            channel="email",
            event_type="deposit_confirmed",
            status="failed",
            retry_count=4,
        )
        session.add(invalid_notification)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    engine.dispose()
