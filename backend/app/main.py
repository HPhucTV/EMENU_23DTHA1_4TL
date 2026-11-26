"""Điểm khởi chạy ứng dụng Python FastAPI — Nhà hàng Ẩm thực Vườn Phố (QL09-W)."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.schemas.system_schemas import HealthResponse
from app.services.system_service import build_health_payload


def create_application() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title=settings.app_name,
        description=(
            "REST API hệ thống đặt bàn, đặt món trước và trợ lý AI cho "
            "**Nhà hàng Ẩm thực Vườn Phố** (TP.HCM · Tiền tệ `VNĐ` · Múi giờ `GMT+7`)."
        ),
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get(
        "/health",
        response_model=HealthResponse,
        tags=["Health"],
        summary="Kiểm tra trạng thái hoạt động của API và kết nối CSDL",
    )
    def health_check() -> HealthResponse:
        return build_health_payload()

    application.include_router(api_v1_router, prefix="/api/v1")

    return application


app = create_application()
