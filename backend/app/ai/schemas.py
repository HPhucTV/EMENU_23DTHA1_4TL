"""Pydantic v2 schemas cho trạng thái sức khỏe Chatbot AI & Ollama (/api/v1/chat/health)."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class LoadedModelMemory(BaseModel):
    """Thông tin model đang nạp trên bộ nhớ từ endpoint `/api/ps` của Ollama."""

    name: str = Field(examples=["gemma3:4b"])
    size_mb: float = Field(ge=0, examples=[2960.5])
    size_vram_mb: float = Field(ge=0, examples=[0.0])
    processor: str = Field(examples=["CPU"])


class ChatHealthResponse(BaseModel):
    """Schema phản hồi cho `GET /api/v1/chat/health`."""

    status: Literal["ok", "degraded", "unavailable"] = Field(
        description="ok khi Ollama sẵn sàng và có ít nhất model chính hoặc dự phòng"
    )
    service: str = "emenu-ai-chatbot"
    ollama_reachable: bool
    ollama_base_url: str = Field(examples=["http://localhost:11434"])
    ollama_version: str | None = Field(default=None, examples=["0.40.18"])
    configured_model: str = Field(examples=["gemma3:4b"])
    fallback_model: str = Field(examples=["llama3.1:8b"])
    active_model: str | None = Field(default=None, examples=["gemma3:4b"])
    model_ready: bool
    fallback_model_ready: bool
    is_fallback: bool = Field(
        description="True khi AI chưa sẵn sàng để Front-end kích hoạt fallback UI"
    )
    available_models: list[str] = Field(default_factory=list)
    loaded_models: list[LoadedModelMemory] = Field(default_factory=list)
    latency_ms: float = Field(ge=0, examples=[12.4])
    timestamp: datetime
    detail: str
