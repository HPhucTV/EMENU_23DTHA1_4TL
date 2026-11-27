"""Kiểm thử tự động cho ai_models.py và migration nhánh AI (MC-71 / WBS 1.3.5.1)."""

from datetime import timedelta, timezone
from io import StringIO
from pathlib import Path
import uuid

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import Base, build_engine
from app.core.timezone import VN_TZ, now_gmt7
from app.models.ai_models import (
    AI_TABLE_NAMES,
    CHAT_RETENTION_DAYS,
    ChatMessage,
    ChatSession,
    KnowledgeDoc,
)
from app.models.core_models import CORE_TABLE_NAMES, User

BACKEND_DIR = Path(__file__).resolve().parents[2]


def _make_alembic_config(database_url: str) -> Config:
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", database_url)
    return cfg


def test_alembic_upgrades_and_downgrades_all_16_tables_with_independent_branches(
    tmp_path: Path,
) -> None:
    cfg = _make_alembic_config("sqlite+pysqlite:///:memory:")
    script_dir = ScriptDirectory.from_config(cfg)

    assert script_dir.as_revision_number("core@head") == "20261126_0001_core"
    assert script_dir.as_revision_number("ai@head") == "20261127_0001_ai"
    assert set(script_dir.get_heads()) == {
        "20261126_0001_core",
        "20261127_0001_ai",
    }

    db_file = tmp_path / "all_16_tables.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"
    file_cfg = _make_alembic_config(db_url)

    command.upgrade(file_cfg, "heads")
    engine = build_engine(db_url)
    try:
        tables = set(inspect(engine).get_table_names())
        expected_all = set(CORE_TABLE_NAMES) | set(AI_TABLE_NAMES)
        assert len(expected_all) == 16
        assert expected_all.issubset(tables)
        assert "alembic_version" in tables
    finally:
        engine.dispose()

    command.downgrade(file_cfg, "base")
    engine_down = build_engine(db_url)
    try:
        remaining = set(inspect(engine_down).get_table_names()) - {
            "alembic_version"
        }
        assert remaining == set()
    finally:
        engine_down.dispose()

    command.upgrade(file_cfg, "heads")
    engine_reup = build_engine(db_url)
    try:
        assert (set(CORE_TABLE_NAMES) | set(AI_TABLE_NAMES)).issubset(
            set(inspect(engine_reup).get_table_names())
        )
    finally:
        engine_reup.dispose()


def test_postgresql_offline_sql_contains_ai_tables_uuid_and_constraints() -> None:
    sql_buffer = StringIO()
    cfg = _make_alembic_config(
        "postgresql+psycopg://emenu_user@localhost:5432/emenu_db"
    )
    cfg.output_buffer = sql_buffer

    command.upgrade(cfg, "heads", sql=True)
    generated_sql = sql_buffer.getvalue()

    for table_name in AI_TABLE_NAMES:
        assert f"CREATE TABLE {table_name}" in generated_sql

    assert "id UUID NOT NULL" in generated_sql
    assert "session_id UUID NOT NULL" in generated_sql
    assert "TIMESTAMP WITH TIME ZONE" in generated_sql
    assert "ON DELETE SET NULL" in generated_sql
    assert "ON DELETE CASCADE" in generated_sql
    assert "ck_knowledge_docs_knowledge_doc_category_valid" in generated_sql
    assert "ck_chat_messages_chat_message_sender_valid" in generated_sql
    assert "ck_chat_messages_chat_message_feedback_valid" in generated_sql
    assert "ck_chat_messages_chat_message_latency_non_negative" in generated_sql


def test_knowledge_docs_crud_check_constraint_and_user_set_null(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "knowledge_docs.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"
    command.upgrade(_make_alembic_config(db_url), "heads")

    engine = build_engine(db_url)
    try:
        with Session(engine) as session:
            manager = User(
                full_name="Quản Lý Vườn Phố",
                email="manager_ai@vuonpho.vn",
                phone="0909888777",
                password_hash="hashed_pw",
                role="manager",
            )
            session.add(manager)
            session.flush()

            docs = [
                KnowledgeDoc(
                    category=cat,
                    title=f"Tài liệu {cat}",
                    content=f"Nội dung chuẩn cho mục {cat}.",
                    updated_by=manager.id,
                )
                for cat in ("faq", "policy", "hours", "info")
            ]
            session.add_all(docs)
            session.commit()

            saved = session.execute(select(KnowledgeDoc)).scalars().all()
            assert len(saved) == 4
            assert all(doc.is_active is True for doc in saved)
            assert all(doc.updater is not None for doc in saved)

            invalid_doc = KnowledgeDoc(
                category="invalid_cat",
                title="Danh mục sai",
                content="Không hợp lệ",
            )
            session.add(invalid_doc)
            with pytest.raises(IntegrityError):
                session.commit()
            session.rollback()

            # Xóa người cập nhật -> giữ nguyên knowledge_docs, updated_by về None (ON DELETE SET NULL)
            session.delete(manager)
            session.commit()

            remaining_docs = session.execute(select(KnowledgeDoc)).scalars().all()
            assert len(remaining_docs) == 4
            assert all(doc.updated_by is None for doc in remaining_docs)
    finally:
        engine.dispose()


def test_chat_sessions_and_messages_uuid_cascade_and_guardrail_checks(
    tmp_path: Path,
) -> None:
    db_file = tmp_path / "chat_sessions.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"
    command.upgrade(_make_alembic_config(db_url), "heads")

    engine = build_engine(db_url)
    try:
        with Session(engine) as session:
            customer = User(
                full_name="Nguyễn Văn Khách",
                email="khach_ai@vuonpho.vn",
                phone="0911222333",
                password_hash="hashed_pw",
                role="customer",
            )
            session.add(customer)
            session.flush()

            guest_session = ChatSession(
                user_id=None,
                context_json={"intent": "menu_advice", "state": "idle"},
            )
            member_session = ChatSession(
                user_id=customer.id,
                context_json={
                    "intent": "reservation",
                    "state": "collecting_info",
                    "slots": {"date": "2026-12-01", "time": "19:00", "guests": 4},
                },
            )
            session.add_all([guest_session, member_session])
            session.flush()

            assert isinstance(guest_session.id, uuid.UUID)
            assert isinstance(member_session.id, uuid.UUID)
            assert guest_session.id != member_session.id

            created_utc = (
                member_session.created_at.replace(tzinfo=timezone.utc)
                if member_session.created_at.tzinfo is None
                else member_session.created_at
            )
            expires_aware = (
                member_session.expires_at.replace(tzinfo=VN_TZ)
                if member_session.expires_at.tzinfo is None
                else member_session.expires_at
            )
            delta = expires_aware - created_utc
            assert timedelta(days=CHAT_RETENTION_DAYS - 1) <= delta <= timedelta(
                days=CHAT_RETENTION_DAYS + 1
            )
            assert expires_aware > now_gmt7()

            user_msg = ChatMessage(
                session_id=member_session.id,
                sender="user",
                masked_content="Đặt bàn 4 người lúc 19:00 ngày 01/12, SĐT [MASKED_PHONE]",
            )
            bot_msg = ChatMessage(
                session_id=member_session.id,
                sender="assistant",
                masked_content="Dạ, em gợi ý bàn khu Sân vườn và món không cay ạ.",
                response_meta_json={
                    "dish_cards": [{"id": 12, "name": "Lẩu gà lá é", "price": 280000}],
                    "booking_prefill_url": "/booking?date=2026-12-01&time=19:00&guests=4",
                },
                feedback="helpful",
                is_fallback=False,
                latency_ms=1450,
            )
            session.add_all([user_msg, bot_msg])
            session.commit()

            refreshed_session = session.get(ChatSession, member_session.id)
            assert refreshed_session is not None
            assert [m.sender for m in refreshed_session.messages] == [
                "user",
                "assistant",
            ]
            assert (
                refreshed_session.messages[1].response_meta_json["dish_cards"][0]["id"]
                == 12
            )

            # Kiểm tra ràng buộc sender, feedback và latency_ms >= 0
            for bad_kwargs in (
                {"sender": "bot", "masked_content": "invalid sender"},
                {
                    "sender": "assistant",
                    "masked_content": "invalid feedback",
                    "feedback": "neutral",
                },
                {
                    "sender": "assistant",
                    "masked_content": "negative latency",
                    "latency_ms": -1,
                },
            ):
                session.add(ChatMessage(session_id=member_session.id, **bad_kwargs))
                with pytest.raises(IntegrityError):
                    session.commit()
                session.rollback()

            # Xóa User -> chat_sessions.user_id thành None (SET NULL), phiên chat vẫn giữ
            session.delete(customer)
            session.commit()
            kept_session = session.get(ChatSession, member_session.id)
            assert kept_session is not None
            assert kept_session.user_id is None

            # Xóa ChatSession -> tự động xóa dây chuyền ChatMessage (CASCADE dọn log 90 ngày)
            session.delete(kept_session)
            session.commit()
            remaining_msgs = (
                session.execute(
                    select(ChatMessage).where(
                        ChatMessage.session_id == member_session.id
                    )
                )
                .scalars()
                .all()
            )
            assert remaining_msgs == []
    finally:
        engine.dispose()


def test_zero_file_overlap_partition_respected() -> None:
    assert set(AI_TABLE_NAMES) == {
        "knowledge_docs",
        "chat_sessions",
        "chat_messages",
    }
    assert set(AI_TABLE_NAMES).isdisjoint(set(CORE_TABLE_NAMES))
    assert (set(CORE_TABLE_NAMES) | set(AI_TABLE_NAMES)).issubset(
        set(Base.metadata.tables.keys())
    )

    core_models_path = BACKEND_DIR / "app" / "models" / "core_models.py"
    core_source = core_models_path.read_text(encoding="utf-8")
    for table_name in AI_TABLE_NAMES:
        assert f'__tablename__ = "{table_name}"' not in core_source
