"""Module trợ lý AI Chatbot (Ollama + Guardrails + RAG) — phân vùng sở hữu của AI Dev."""

from app.ai.config import AISettings, get_ai_settings
from app.ai.ollama_client import (
    OllamaChatResult,
    OllamaClient,
    OllamaError,
    OllamaHealthStatus,
    OllamaTimeoutError,
    OllamaUnavailableError,
)

__all__ = [
    "AISettings",
    "OllamaChatResult",
    "OllamaClient",
    "OllamaError",
    "OllamaHealthStatus",
    "OllamaTimeoutError",
    "OllamaUnavailableError",
    "get_ai_settings",
]
