""" Kiểm thử tự động cho US-01: /health, Swagger, kết nối SQLAlchemy DB và API mẫu."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.core import database as db_module
from app.core.database import build_engine
from app.main import app


def test_health_endpoint_returns_200_with_connected_db(monkeypatch) -> None:
    test_engine = build_engine("sqlite+pysqlite:///:memory:")
    monkeypatch.setattr(db_module, "engine", test_engine)

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["timezone"] == "Asia/Ho_Chi_Minh"
    assert body["utc_offset"] == "GMT+7"
    assert body["currency"] == "VND"
    assert body["database"]["status"] == "connected"


def test_swagger_ui_and_openapi_schema_available() -> None:
    client = TestClient(app)

    docs_res = client.get("/docs")
    assert docs_res.status_code == 200
    assert "swagger-ui" in docs_res.text.lower()

    openapi_res = client.get("/openapi.json")
    assert openapi_res.status_code == 200
    paths = openapi_res.json()["paths"]
    assert "/health" in paths
    assert "/api/v1/system/overview" in paths
    assert "/api/v1/system/db-check" in paths


def test_system_overview_and_db_check_endpoints(monkeypatch) -> None:
    test_engine = build_engine("sqlite+pysqlite:///:memory:")
    monkeypatch.setattr(db_module, "engine", test_engine)

    client = TestClient(app)

    overview_res = client.get("/api/v1/system/overview")
    assert overview_res.status_code == 200
    data = overview_res.json()
    assert data["restaurant_name"] == "Nhà hàng Ẩm thực Vườn Phố"
    assert data["currency"] == "VND"
    assert len(data["areas"]) == 3
    assert len(data["signature_dishes"]) >= 3
    assert data["signature_dishes"][0]["price_formatted"].endswith("₫")
    assert data["booking_rules"]["slot_step_minutes"] == 30
    assert data["booking_rules"]["dining_duration_minutes"] == 90
    assert data["booking_rules"]["hold_minutes"] == 10

    db_res = client.get("/api/v1/system/db-check")
    assert db_res.status_code == 200
    assert db_res.json()["status"] == "connected"


def test_db_check_returns_503_when_database_unreachable(monkeypatch) -> None:
    broken_engine = create_engine(
        "postgresql+psycopg://invalid:invalid@127.0.0.1:1/nonexistent",
        connect_args={"connect_timeout": 1},
    )
    monkeypatch.setattr(db_module, "engine", broken_engine)

    client = TestClient(app)

    # /health vẫn trả 200 để báo tiến trình API sống kèm trạng thái DB disconnected
    health_res = client.get("/health")
    assert health_res.status_code == 200
    assert health_res.json()["database"]["status"] == "disconnected"

    # /api/v1/system/db-check trả 503 khi DB chưa sẵn sàng
    db_res = client.get("/api/v1/system/db-check")
    assert db_res.status_code == 503
    assert db_res.json()["status"] == "disconnected"
