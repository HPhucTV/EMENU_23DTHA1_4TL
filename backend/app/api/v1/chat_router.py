"""Router API Chatbot AI (`/api/v1/chat/*`) — phân vùng sở hữu của AI Dev."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.ai.ollama_client import OllamaClient
from app.ai.schemas import ChatHealthResponse, LoadedModelMemory
from app.core.timezone import now_gmt7

# router.py tự động gắn prefix="/api/v1" khi router này có prefix="/chat"
router = APIRouter(prefix="/chat")


def get_ollama_client() -> OllamaClient:
    """Dependency cung cấp OllamaClient cho các endpoint `/api/v1/chat/*`."""
    return OllamaClient()


@router.get(
    "/health",
    response_model=ChatHealthResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ChatHealthResponse,
            "description": "Ollama chưa kết nối được hoặc chưa sẵn sàng model",
        }
    },
    summary="Kiểm tra kết nối máy chủ Ollama và model AI sẵn sàng",
)
async def chat_health_check(
    client: OllamaClient = Depends(get_ollama_client),
) -> ChatHealthResponse | JSONResponse:
    """Trả về HTTP 200 khi Ollama sẵn sàng phục vụ, hoặc 503 kèm `is_fallback=true` khi gián đoạn."""
    health = await client.check_health()
    payload = ChatHealthResponse(
        status=health.status,  # type: ignore[arg-type]
        ollama_reachable=health.ollama_reachable,
        ollama_base_url=health.ollama_base_url,
        ollama_version=health.ollama_version,
        configured_model=health.configured_model,
        fallback_model=health.fallback_model,
        active_model=health.active_model,
        model_ready=health.model_ready,
        fallback_model_ready=health.fallback_model_ready,
        is_fallback=health.is_fallback,
        available_models=health.available_models,
        loaded_models=[LoadedModelMemory(**item) for item in health.loaded_models],
        latency_ms=health.latency_ms,
        timestamp=now_gmt7(),
        detail=health.detail,
    )
    if health.status != "ok":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=payload.model_dump(mode="json"),
        )
    return payload
