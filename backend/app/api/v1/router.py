"""Bộ định tuyến tổng hợp cho REST API v1."""

from fastapi import APIRouter

from app.api.v1.auth_router import router as auth_router
from app.api.v1.system_router import router as system_router
from app.api.v1.users_router import router as users_router

api_v1_router = APIRouter()
api_v1_router.include_router(system_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)

# Tự động gắn chat_router khi AI Dev triển khai `backend/app/api/v1/chat_router.py`
# mà không cần chỉnh sửa file vùng Core của Dev Fullstack (Zero File-Overlap).
try:
    from app.api.v1.chat_router import router as chat_router  # type: ignore[import-not-found]

    router_prefix = getattr(chat_router, "prefix", "") or ""
    if router_prefix.startswith("/api/v1"):
        # Đã có sẵn tiền tố đầy đủ -> được gắn ở main.py nếu cần
        pass
    elif router_prefix.startswith("/chat"):
        api_v1_router.include_router(chat_router, tags=["AI Chatbot"])
    else:
        api_v1_router.include_router(
            chat_router, prefix="/chat", tags=["AI Chatbot"]
        )
except ModuleNotFoundError:
    pass
