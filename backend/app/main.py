"""Điểm khởi chạy ứng dụng Python FastAPI — Nhà hàng Ẩm thực Vườn Phố (QL09-W)."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import get_settings
from app.schemas.system_schemas import HealthResponse
from app.services.system_service import build_health_payload


def _translate_validation_message(raw_msg: str) -> str:
    cleaned = raw_msg.removeprefix("Value error, ").strip()
    if cleaned == "Field required":
        return "Vui lòng không để trống thông tin bắt buộc này."
    if cleaned.startswith("String should have at least"):
        return "Nội dung nhập vào quá ngắn."
    return cleaned


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

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        field_errors: dict[str, str] = {}
        for err in exc.errors():
            loc = [str(part) for part in err.get("loc", ()) if part != "body"]
            msg = _translate_validation_message(str(err.get("msg", "Dữ liệu không hợp lệ.")))
            field_name = loc[-1] if loc else (
                "confirm_password" if "xác nhận" in msg.lower() else "form"
            )
            field_errors.setdefault(field_name, msg)

        first_message = next(
            iter(field_errors.values()),
            "Vui lòng kiểm tra lại thông tin đã nhập.",
        )
        return JSONResponse(
            status_code=422,
            content={
                "detail": {
                    "code": "VALIDATION_ERROR",
                    "message": first_message,
                    "field_errors": field_errors,
                }
            },
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
