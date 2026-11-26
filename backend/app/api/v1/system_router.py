"""Endpoints kiểm tra CSDL và dữ liệu tổng quan mẫu cho Front-end (US-01)."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.database import check_database_health
from app.schemas.system_schemas import DatabaseHealth, RestaurantOverviewResponse
from app.services.system_service import build_restaurant_overview

router = APIRouter(prefix="/system", tags=["System"])


@router.get(
    "/overview",
    response_model=RestaurantOverviewResponse,
    summary="Lấy thông tin tổng quan nhà hàng và quy tắc đặt bàn mặc định",
)
def get_restaurant_overview() -> RestaurantOverviewResponse:
    """API mẫu (US-01) để Front-end ReactJS kiểm chứng kết nối tới Back-end."""
    return build_restaurant_overview()


@router.get(
    "/db-check",
    response_model=DatabaseHealth,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": DatabaseHealth,
            "description": "Chưa kết nối được PostgreSQL",
        }
    },
    summary="Kiểm tra kết nối trực tiếp tới PostgreSQL (SELECT 1)",
)
def verify_database_connection() -> DatabaseHealth | JSONResponse:
    """Trả về 200 khi CSDL phản hồi SELECT 1, hoặc 503 khi chưa kết nối được."""
    result = DatabaseHealth(**check_database_health())
    if result.status != "connected":
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=result.model_dump(),
        )
    return result
