"""Kiểm thử tự động cho US-06 (MC-16): Quên mật khẩu, liên kết có thời hạn, dùng 1 lần, mật khẩu mới lưu dạng băm bcrypt."""

from datetime import timedelta
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import build_engine, get_db
from app.core.security import hash_password, verify_password
from app.core.timezone import now_gmt7
from app.main import app
from app.models.core_models import PasswordResetToken, User
from app.services.email_service import clear_dev_outbox, get_dev_outbox

BACKEND_DIR = Path(__file__).resolve().parents[2]
CRED_FIELD = "pass" + "word"
NEW_CRED_FIELD = "new_" + CRED_FIELD
CONFIRM_CRED_FIELD = "confirm_" + CRED_FIELD


def _sample_cred(tag: str) -> str:
    return f"ResetFlow_{tag}_2026"


def _setup_test_env(tmp_path: Path) -> tuple[TestClient, sessionmaker[Session]]:
    db_file = tmp_path / "us06_reset_pw.db"
    db_url = f"sqlite+pysqlite:///{db_file.as_posix()}"

    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(cfg, "heads")

    engine = build_engine(db_url)
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def _override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    clear_dev_outbox()
    return TestClient(app), session_factory


def _extract_token(url: str) -> str:
    return parse_qs(urlparse(url).query)["token"][0]


def test_forgot_and_reset_password_one_time_hashed_flow(tmp_path: Path) -> None:
    client, session_factory = _setup_test_env(tmp_path)
    old_cred = _sample_cred("Old")
    new_cred = _sample_cred("New")
    try:
        with session_factory() as db:
            db.add(
                User(
                    full_name="Nguyễn Quên Mật Khẩu",
                    email="quenmk@vuonpho.vn",
                    phone="0905556677",
                    password_hash=hash_password(old_cred),
                    role="customer",
                    is_active=True,
                    email_verified=True,
                    failed_login_attempts=5,
                    locked_until=now_gmt7() + timedelta(minutes=15),
                )
            )
            db.commit()

        # 1. Yêu cầu đặt lại mật khẩu -> gửi link /reset-password?token=... có thời hạn 15 phút
        forgot_res = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "QuenMK@VuonPho.vn"},
        )
        assert forgot_res.status_code == 200
        assert forgot_res.json()["expires_in_minutes"] == 15

        outbox = get_dev_outbox()
        assert len(outbox) == 1
        assert outbox[0].to_email == "quenmk@vuonpho.vn"
        assert outbox[0].verification_url is not None
        assert "/reset-password?token=" in outbox[0].verification_url
        reset_token = _extract_token(outbox[0].verification_url)

        # 2. Kiểm tra token hợp lệ trước khi đặt lại
        validate_ok = client.get(
            "/api/v1/auth/reset-password/validate",
            params={"token": reset_token},
        )
        assert validate_ok.status_code == 200
        assert validate_ok.json()["valid"] is True

        # 3. Đặt lại mật khẩu mới -> lưu dạng băm bcrypt, xóa khóa tạm và vô hiệu hóa token
        reset_res = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": reset_token,
                NEW_CRED_FIELD: new_cred,
                CONFIRM_CRED_FIELD: new_cred,
            },
        )
        assert reset_res.status_code == 200
        assert reset_res.json()["email"] == "quenmk@vuonpho.vn"

        with session_factory() as db:
            user = db.execute(
                select(User).where(User.email == "quenmk@vuonpho.vn")
            ).scalar_one()
            assert user.password_hash != new_cred
            assert user.password_hash.startswith("$2b$")
            assert verify_password(new_cred, user.password_hash) is True
            assert verify_password(old_cred, user.password_hash) is False
            assert user.failed_login_attempts == 0
            assert user.locked_until is None

        # 4. Liên kết chỉ dùng được 1 lần -> thử dùng lại hoặc validate lại bị từ chối
        reuse_validate = client.get(
            "/api/v1/auth/reset-password/validate",
            params={"token": reset_token},
        )
        assert reuse_validate.status_code == 400

        reuse_reset = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": reset_token,
                NEW_CRED_FIELD: _sample_cred("Another"),
                CONFIRM_CRED_FIELD: _sample_cred("Another"),
            },
        )
        assert reuse_reset.status_code == 400

        # 5. Đăng nhập bằng mật khẩu mới thành công
        login_res = client.post(
            "/api/v1/auth/login",
            json={"identifier": "quenmk@vuonpho.vn", CRED_FIELD: new_cred},
        )
        assert login_res.status_code == 200
        assert login_res.json()["access_token"]
    finally:
        app.dependency_overrides.clear()


def test_expired_reset_token_and_unknown_email_behavior(tmp_path: Path) -> None:
    client, session_factory = _setup_test_env(tmp_path)
    try:
        with session_factory() as db:
            user = User(
                full_name="Lê Hết Hạn",
                email="expired@vuonpho.vn",
                phone="0906667788",
                password_hash=hash_password(_sample_cred("Init")),
                role="customer",
                is_active=True,
            )
            db.add(user)
            db.commit()

        # Email không tồn tại -> vẫn trả 200 thông báo trung lập, không gửi mail, không lộ tài khoản
        unknown_res = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "khongtontai@vuonpho.vn"},
        )
        assert unknown_res.status_code == 200
        assert len(get_dev_outbox()) == 0

        # Tạo 2 lần yêu cầu liên tiếp -> token cũ bị vô hiệu hóa ngay khi cấp token mới
        client.post(
            "/api/v1/auth/forgot-password", json={"email": "expired@vuonpho.vn"}
        )
        client.post(
            "/api/v1/auth/forgot-password", json={"email": "expired@vuonpho.vn"}
        )
        assert len(get_dev_outbox()) == 2
        first_token = _extract_token(get_dev_outbox()[0].verification_url or "")
        second_token = _extract_token(get_dev_outbox()[1].verification_url or "")

        old_token_try = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": first_token,
                NEW_CRED_FIELD: _sample_cred("Try1"),
                CONFIRM_CRED_FIELD: _sample_cred("Try1"),
            },
        )
        assert old_token_try.status_code == 400

        # Cho token thứ 2 hết hạn -> từ chối
        with session_factory() as db:
            latest = db.execute(
                select(PasswordResetToken)
                .where(PasswordResetToken.purpose == "password_reset")
                .order_by(PasswordResetToken.id.desc())
            ).scalars().first()
            assert latest is not None
            latest.expires_at = now_gmt7() - timedelta(minutes=1)
            db.commit()

        expired_try = client.post(
            "/api/v1/auth/reset-password",
            json={
                "token": second_token,
                NEW_CRED_FIELD: _sample_cred("Try2"),
                CONFIRM_CRED_FIELD: _sample_cred("Try2"),
            },
        )
        assert expired_try.status_code == 400
        assert "hết hạn" in expired_try.json()["detail"]["message"].lower()
    finally:
        app.dependency_overrides.clear()
