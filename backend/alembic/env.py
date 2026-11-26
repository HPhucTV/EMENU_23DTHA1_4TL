"""Môi trường chạy Alembic Migration hỗ trợ kiến trúc Zero File-Overlap."""

from logging.config import fileConfig

from alembic import context

from app.core.config import get_settings
from app.core.database import Base, build_engine
import app.models.core_models  # noqa: F401 — Đăng ký 13 bảng Core vào Base.metadata

# Tự động nạp thêm 3 bảng AI nếu AI Dev đã tạo `app/models/ai_models.py`
# mà không cần chỉnh sửa file vùng Core.
try:
    import app.models.ai_models  # type: ignore[import-not-found]  # noqa: F401
except ModuleNotFoundError:
    pass

config = context.config

if config.config_file_name is not None and config.get_section("loggers") is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _resolve_database_url() -> str:
    configured_url = (config.get_main_option("sqlalchemy.url") or "").strip()
    if configured_url:
        return configured_url
    return get_settings().sqlalchemy_database_url


def run_migrations_offline() -> None:
    """Chạy migration ở chế độ offline (xuất câu lệnh SQL mà không cần nối DB)."""
    url = _resolve_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        output_buffer=config.output_buffer,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Chạy migration trực tiếp trên kết nối CSDL thực tế."""
    connectable = config.attributes.get("connection")

    if connectable is None:
        engine = build_engine(_resolve_database_url())
        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                render_as_batch=connection.dialect.name == "sqlite",
            )
            with context.begin_transaction():
                context.run_migrations()
        engine.dispose()
    else:
        context.configure(
            connection=connectable,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=connectable.dialect.name == "sqlite",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
