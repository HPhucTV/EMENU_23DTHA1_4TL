"""Cấu hình trung tâm của Back-end (Pydantic Settings v2)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nhà hàng Ẩm thực Vườn Phố — E-Menu API"
    app_env: str = "development"
    app_version: str = "0.1.0"
    restaurant_name: str = "Nhà hàng Ẩm thực Vườn Phố"
    timezone: str = "Asia/Ho_Chi_Minh"
    currency: str = "VND"

    database_url: str = "postgresql+psycopg://emenu_user@localhost:5432/emenu_db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    jwt_secret_key: str = "changeme"
    jwt_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def sqlalchemy_database_url(self) -> str:
        """Chuẩn hóa URL PostgreSQL sang driver psycopg v3 cho SQLAlchemy 2.0."""
        url = self.database_url.strip()
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+psycopg://", 1)
        return url

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
