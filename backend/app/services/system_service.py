"""Service cung cấp thông tin sức khỏe hệ thống và dữ liệu mẫu khung dự án (US-01)."""

from sqlalchemy.engine import Engine

from app.core.config import get_settings
from app.core.database import check_database_health
from app.core.timezone import format_vnd, now_gmt7
from app.schemas.system_schemas import (
    AreaHighlight,
    BookingRuleSummary,
    DatabaseHealth,
    DishPreview,
    HealthResponse,
    RestaurantOverviewResponse,
)


def build_health_payload(target_engine: Engine | None = None) -> HealthResponse:
    settings = get_settings()
    db_info = DatabaseHealth(**check_database_health(target_engine))
    return HealthResponse(
        status="ok",
        service="emenu-backend",
        restaurant=settings.restaurant_name,
        version=settings.app_version,
        environment=settings.app_env,
        timezone=settings.timezone,
        utc_offset="GMT+7",
        currency=settings.currency,
        timestamp=now_gmt7(),
        database=db_info,
    )


def build_restaurant_overview(
    target_engine: Engine | None = None,
) -> RestaurantOverviewResponse:
    settings = get_settings()
    db_info = DatabaseHealth(**check_database_health(target_engine))

    sample_dishes = [
        (
            "VP-M01",
            "Món chính",
            "Bò cuốn lá lốt",
            "Bò nướng thơm lá lốt, dùng kèm rau sống và mắm nêm đậm vị Việt.",
            185_000,
        ),
        (
            "VP-M02",
            "Khai vị · Hải sản",
            "Gỏi ngó sen tôm",
            "Ngó sen giòn thanh mát trộn tôm tươi, rau răm và nước mắm chua ngọt.",
            145_000,
        ),
        (
            "VP-M03",
            "Món chính",
            "Cơm chiên trái thơm",
            "Cơm chiên hạt điều, rau củ và hải sản trình bày trong trái thơm chín.",
            125_000,
        ),
        (
            "VP-M04",
            "Món chay",
            "Nấm kho tiêu",
            "Nấm đùi gà và đậu hũ kho niêu đất dậy mùi tiêu xanh ấm nồng.",
            95_000,
        ),
    ]

    return RestaurantOverviewResponse(
        restaurant_name=settings.restaurant_name,
        tagline="Một chốn xanh, vạn vị thân quen.",
        city="TP. Hồ Chí Minh",
        timezone="Asia/Ho_Chi_Minh (GMT+7)",
        currency=settings.currency,
        server_time_gmt7=now_gmt7(),
        database=db_info,
        areas=[
            AreaHighlight(
                code="SV",
                name="Sân vườn",
                summary="Khoáng đạt, rợp bóng cây xanh và đèn lồng ấm áp.",
                capacity_hint="Bàn 2 – 8 khách, hỗ trợ ghép bàn",
            ),
            AreaHighlight(
                code="TT",
                name="Tầng trệt",
                summary="Không gian ấm cúng cho những bữa cơm gia đình sum họp.",
                capacity_hint="Bàn 2 – 6 khách",
            ),
            AreaHighlight(
                code="VIP",
                name="Phòng riêng VIP",
                summary="Riêng tư, yên tĩnh cho cuộc hẹn đối tác và tiệc thân mật.",
                capacity_hint="Phòng 6 – 12 khách",
            ),
        ],
        signature_dishes=[
            DishPreview(
                code=code,
                category=category,
                name=name,
                description=desc,
                price_vnd=price,
                price_formatted=format_vnd(price),
                status="available",
            )
            for code, category, name, desc, price in sample_dishes
        ],
        booking_rules=BookingRuleSummary(
            slot_step_minutes=30,
            dining_duration_minutes=90,
            hold_minutes=10,
            min_advance_hours=2,
            max_advance_days=30,
            default_deposit_percent=30,
        ),
    )
