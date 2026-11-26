"""Kiểm thử tự động cho US-04 (MC-14): Đăng ký tài khoản, băm mật khẩu bcrypt, chống trùng email/SĐT, gửi & xác thực email."""

from datetime import timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import build_engine, get_db
from app.core.security import hash_one_time_token, verify_password
from app.core.timezone import now_gmt7
from app.main import app
from app.models.core_models import PasswordResetToken, User
from app.services.email_service import clear_dev_outbox, get_dev_outbox

BACKEND_DIR = Path(__file__).resolve().parents[2]


def _setup_test_client(tmp_path: Path) -> tuple[TestClient, sessionmaker[Session]]:
    db_file = tmp_path / "us04_auth.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"

    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(cfg, "heads")

    engine = build_engine(db_url)
    testing_session_local = sessionmaker(
        bind=engine, autoflush=False, autocommit=False
    )

    def _override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    clear_dev_outbox()
    return TestClient(app), testing_session_local


def _extract_token_from_outbox_url(url: str) -> str:
    parsed = urlparse(url)
    return parse_qs(parsed.query)["token"][0]


def test_register_hashes_password_and_sends_verification_email(
    tmp_path: Path,
) -> None:
    client, session_factory = _setup_test_client(tmp_path)
    try:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "  Nguyễn   Văn Tiến  ",
                "phone": "+84 901 234 567",
                "email": "Tien.Nguyen@Example.com ",
                "password": "VuonPho2026",
                "confirm_password": "VuonPho2026",
                "accepted_terms": True,
            },
        )

        assert response.status_code == 201
        body = response.json()
        assert body["verification_email_sent"] is True
        assert body["user"]["full_name"] == "Nguyễn Văn Tiến"
        assert body["user"]["phone"] == "0901234567"
        assert body["user"]["email"] == "tien.nguyen@example.com"
        assert body["user"]["role"] == "customer"
        assert body["user"]["email_verified"] is False
        assert "password" not in body["user"]
        assert "password_hash" not in body["user"]

        # Kiểm tra mật khẩu trong CSDL lưu dạng băm bcrypt (không lưu plain text)
        with session_factory() as db:
            saved_user = db.execute(
                select(User).where(User.email == "tien.nguyen@example.com")
            ).scalar_one()
            assert saved_user.password_hash != "VuonPho2026"
            assert saved_user.password_hash.startswith("$2b$")
            assert verify_password("VuonPho2026", saved_user.password_hash) is True

        # Kiểm tra email xác thực đã được gửi đi kèm link dùng 1 lần
        outbox = get_dev_outbox()
        assert len(outbox) == 1
        assert outbox[0].to_email == "tien.nguyen@example.com"
        assert outbox[0].verification_url is not None
        assert "/verify-email?token=" in outbox[0].verification_url
    finally:
        app.dependency_overrides.clear()


def test_register_rejects_duplicate_email_and_duplicate_phone(
    tmp_path: Path,
) -> None:
    client, _ = _setup_test_client(tmp_path)
    try:
        first = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Khách Đầu Tiên",
                "phone": "0909111222",
                "email": "khach1@vuonpho.vn",
                "password": "MatKhau123",
                "confirm_password": "MatKhau123",
                "accepted_terms": True,
            },
        )
        assert first.status_code == 201

        # Trùng email
        dup_email = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Khách Trùng Email",
                "phone": "0912333444",
                "email": "KHACH1@vuonpho.vn",
                "password": "MatKhau123",
                "confirm_password": "MatKhau123",
                "accepted_terms": True,
            },
        )
        assert dup_email.status_code == 409
        email_err = dup_email.json()["detail"]
        assert email_err["code"] == "DUPLICATE_ACCOUNT"
        assert "email" in email_err["field_errors"]

        # Trùng số điện thoại (dù nhập dạng +84)
        dup_phone = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Khách Trùng SĐT",
                "phone": "+84-909-111-222",
                "email": "khach_moi@vuonpho.vn",
                "password": "MatKhau123",
                "confirm_password": "MatKhau123",
                "accepted_terms": True,
            },
        )
        assert dup_phone.status_code == 409
        phone_err = dup_phone.json()["detail"]
        assert "phone" in phone_err["field_errors"]
    finally:
        app.dependency_overrides.clear()


def test_register_returns_clear_field_errors_for_invalid_inputs(
    tmp_path: Path,
) -> None:
    client, _ = _setup_test_client(tmp_path)
    try:
        invalid_res = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "A",
                "phone": "12345",
                "email": "sai-dinh-dang-email",
                "password": "ngan",
                "confirm_password": "khac",
                "accepted_terms": False,
            },
        )
        assert invalid_res.status_code == 422
        detail = invalid_res.json()["detail"]
        assert detail["code"] == "VALIDATION_ERROR"
        field_errors = detail["field_errors"]
        assert "full_name" in field_errors
        assert "phone" in field_errors
        assert "email" in field_errors
        assert "password" in field_errors
        assert "accepted_terms" in field_errors

        # Kiểm tra lệch mật khẩu xác nhận khi các trường khác đã hợp lệ
        mismatch_res = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Trần Văn B",
                "phone": "0988777666",
                "email": "tranvanb@vuonpho.vn",
                "password": "MatKhau123",
                "confirm_password": "MatKhau999",
                "accepted_terms": True,
            },
        )
        assert mismatch_res.status_code == 422
        assert (
            "confirm_password" in mismatch_res.json()["detail"]["field_errors"]
        )
    finally:
        app.dependency_overrides.clear()


def test_verify_email_one_time_token_and_resend_flow(tmp_path: Path) -> None:
    client, session_factory = _setup_test_client(tmp_path)
    try:
        reg_res = client.post(
            "/api/v1/auth/register",
            json={
                "full_name": "Lê Thị Hương",
                "phone": "0933444555",
                "email": "huong@vuonpho.vn",
                "password": "VuonPho2026",
                "confirm_password": "VuonPho2026",
                "accepted_terms": True,
            },
        )
        assert reg_res.status_code == 201
        first_url = get_dev_outbox()[0].verification_url
        assert first_url is not None
        first_token = _extract_token_from_outbox_url(first_url)

        # Gửi lại email xác thực -> token cũ bị vô hiệu hóa, token mới hoạt động
        resend_res = client.post(
            "/api/v1/auth/resend-verification",
            json={"email": "huong@vuonpho.vn"},
        )
        assert resend_res.status_code == 200
        assert len(get_dev_outbox()) == 2
        second_url = get_dev_outbox()[1].verification_url
        assert second_url is not None
        second_token = _extract_token_from_outbox_url(second_url)

        old_try = client.post(
            "/api/v1/auth/verify-email", json={"token": first_token}
        )
        assert old_try.status_code == 400

        verify_ok = client.post(
            "/api/v1/auth/verify-email", json={"token": second_token}
        )
        assert verify_ok.status_code == 200
        assert verify_ok.json()["email_verified"] is True

        # Dùng lại lần 2 trên cùng token -> từ chối
        reuse_try = client.post(
            "/api/v1/auth/verify-email", json={"token": second_token}
        )
        assert reuse_try.status_code == 400

        with session_factory() as db:
            user = db.execute(
                select(User).where(User.email == "huong@vuonpho.vn")
            ).scalar_one()
            assert user.email_verified is True

            # Kiểm tra token hết hạn trả lỗi rõ ràng
            expired_raw = "expired_token_value_123456"
            expired_record = PasswordResetToken(
                user_id=user.id,
                token_hash=hash_one_time_token(expired_raw),
                purpose="email_verify",
                expires_at=now_gmt7() - timedelta(minutes=5),
            )
            db.add(expired_record)
            db.commit()

        expired_try = client.post(
            "/api/v1/auth/verify-email", json={"token": expired_raw}
        )
        assert expired_try.status_code == 400
        assert "hết hạn" in expired_try.json()["detail"]["message"].lower()
    finally:
        app.dependency_overrides.clear()
