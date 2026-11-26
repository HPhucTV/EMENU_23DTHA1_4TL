"""Schemas kiểm tra sức khỏe hệ thống và API tổng quan mẫu (US-01)."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class DatabaseHealth(BaseModel):
    status: Literal["connected", "disconnected"] = Field(
        description="Trạng thái kết nối thực tế tới CSDL"
    )
    dialect: str = Field(examples=["postgresql"])
    latency_ms: float = Field(examples=[1.85])
    detail: str = Field(examples=["Kết nối cơ sở dữ liệu sẵn sàng."])


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "emenu-backend"
    restaurant: str = "Nhà hàng Ẩm thực Vườn Phố"
    version: str = "0.1.0"
    environment: str = "development"
    timezone: str = "Asia/Ho_Chi_Minh"
    utc_offset: str = "GMT+7"
    currency: str = "VND"
    timestamp: datetime
    database: DatabaseHealth


class AreaHighlight(BaseModel):
    code: str
    name: str
    summary: str
    capacity_hint: str


class DishPreview(BaseModel):
    code: str
    category: str
    name: str
    description: str
    price_vnd: int = Field(gt=0, description="Giá niêm yết tính bằng VNĐ")
    price_formatted: str = Field(examples=["185.000 ₫"])
    status: Literal["available", "out_of_stock"] = "available"


class BookingRuleSummary(BaseModel):
    slot_step_minutes: int = 30
    dining_duration_minutes: int = 90
    hold_minutes: int = 10
    min_advance_hours: int = 2
    max_advance_days: int = 30
    default_deposit_percent: int = 30


class RestaurantOverviewResponse(BaseModel):
    restaurant_name: str
    tagline: str
    city: str
    timezone: str
    currency: str
    server_time_gmt7: datetime
    database: DatabaseHealth
    areas: list[AreaHighlight]
    signature_dishes: list[DishPreview]
    booking_rules: BookingRuleSummary
