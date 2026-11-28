"""Cấu hình tích hợp Ollama cho Chatbot AI (Pydantic Settings v2 — phân vùng AI Dev)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class AISettings(BaseSettings):
    """Tham số kết nối và suy luận của dịch vụ Ollama self-hosted."""

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma3:4b"
    ollama_fallback_model: str = "llama3.1:8b"
    ollama_timeout_seconds: float = 30.0
    ollama_health_timeout_seconds: float = 3.0
    ollama_keep_alive: str = "10m"
    ollama_temperature: float = 0.2
    ollama_num_predict: int = 256

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def normalized_base_url(self) -> str:
        """Chuẩn hóa URL gốc của Ollama không có dấu `/` ở cuối."""
        return self.ollama_base_url.strip().rstrip("/")


@lru_cache
def get_ai_settings() -> AISettings:
    """Trả về bản cấu hình AI đã cache cho toàn bộ ứng dụng."""
    return AISettings()
