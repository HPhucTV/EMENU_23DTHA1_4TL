"""Quản lý kết nối CSDL SQLAlchemy 2.0 và kiểm tra sức khỏe PostgreSQL."""

from collections.abc import Generator
from time import perf_counter
from typing import Any

from sqlalchemy import MetaData, create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Lớp cơ sở cho các bảng ORM (dùng chung quy ước đặt tên constraint Alembic)."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def build_engine(database_url: str) -> Engine:
    """Khởi tạo SQLAlchemy Engine kèm đồng bộ múi giờ GMT+7 cho PostgreSQL."""
    connect_args: dict[str, Any] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    elif database_url.startswith("postgresql"):
        connect_args["connect_timeout"] = 3

    db_engine = create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args=connect_args,
    )

    if db_engine.dialect.name == "postgresql":

        @event.listens_for(db_engine, "connect")
        def _set_postgresql_timezone(dbapi_connection: Any, _: Any) -> None:
            with dbapi_connection.cursor() as cursor:
                cursor.execute("SET TIME ZONE 'Asia/Ho_Chi_Minh'")

    return db_engine


settings = get_settings()
engine: Engine = build_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """Dependency cung cấp phiên làm việc CSDL cho FastAPI endpoint."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_health(target_engine: Engine | None = None) -> dict[str, Any]:
    """Thực thi SELECT 1 để xác minh kết nối thực tế tới CSDL."""
    active_engine = target_engine or engine
    dialect_name = active_engine.dialect.name
    started = perf_counter()
    try:
        with active_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        latency_ms = round((perf_counter() - started) * 1000, 2)
        return {
            "status": "connected",
            "dialect": dialect_name,
            "latency_ms": latency_ms,
            "detail": "Kết nối cơ sở dữ liệu sẵn sàng.",
        }
    except SQLAlchemyError as exc:
        latency_ms = round((perf_counter() - started) * 1000, 2)
        return {
            "status": "disconnected",
            "dialect": dialect_name,
            "latency_ms": latency_ms,
            "detail": (
                "Chưa kết nối được PostgreSQL. Hãy khởi động container "
                "`docker compose up -d postgres` hoặc kiểm tra DATABASE_URL. "
                f"({exc.__class__.__name__})"
            ),
        }
