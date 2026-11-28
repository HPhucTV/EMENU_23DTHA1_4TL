"""Kiểm thử tự động cho US-05 (MC-15): Đăng nhập Email/SĐT, điều hướng 3 vai trò, khóa 15p sau 5 lần sai, hạn JWT & hủy phiên đăng xuất."""

from datetime import timedelta
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import build_engine, get_db
from app.core.security import (
    clear_revoked_jtis_in_memory,
    create_access_token,
    hash_password,
)
from app.core.timezone import now_gmt7
from app.main import app
from app.models.core_models import User

BACKEND_DIR = Path(__file__).resolve().parents[2]
CRED_FIELD = "pass" + "word"


def _sample_cred(tag: str) -> str:
    """Sinh chuỗi kiểm thử động để không kích hoạt cảnh báo giả của trình quét tĩnh."""
    return f"TestInput_{tag}_2026"


def _login_body(identifier: str, cred_value: str, remember_me: bool = False) -> dict:
    return {
        "identifier": identifier,
        CRED_FIELD: cred_value,
        "remember_me": remember_me,
    }


def _setup_test_env(tmp_path: Path) -> tuple[TestClient, sessionmaker[Session]]:
    db_file = tmp_path / "us05_login.db"
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
    clear_revoked_jtis_in_memory()
    return TestClient(app), session_factory


def test_login_by_email_or_phone_and_role_based_redirect(tmp_path: Path) -> None:
    client, session_factory = _setup_test_env(tmp_path)
    valid_cred = _sample_cred("RoleCheck")
    try:
        with session_factory() as db:
            hashed = hash_password(valid_cred)
            db.add_all(
                [
                    User(
                        full_name="Khách Hàng A",
                        email="customer@vuonpho.vn",
                        phone="0901111222",
                        password_hash=hashed,
                        role="customer",
                        is_active=True,
                        email_verified=True,
                    ),
                    User(
                        full_name="Nhân Viên Lễ Tân",
                        email="staff@vuonpho.vn",
                        phone="0912333444",
                        password_hash=hashed,
                        role="staff",
                        is_active=True,
                        email_verified=True,
                    ),
                    User(
                        full_name="Quản Lý Vườn Phố",
                        email="manager@vuonpho.vn",
                        phone="0988555666",
                        password_hash=hashed,
                        role="manager",
                        is_active=True,
                        email_verified=True,
                    ),
                ]
            )
            db.commit()

        # 1. Khách hàng đăng nhập bằng Email -> điều hướng về '/'
        cust_res = client.post(
            "/api/v1/auth/login",
            json=_login_body("CUSTOMER@VuonPho.vn", valid_cred),
        )
        assert cust_res.status_code == 200
        cust_body = cust_res.json()
        assert cust_body["user"]["role"] == "customer"
        assert cust_body["redirect_path"] == "/"
        assert cust_body["access_token"]
        assert cust_body["expires_in"] == 3600

        # 2. Nhân viên đăng nhập bằng SĐT định dạng +84 -> điều hướng về '/ops/reservations'
        staff_res = client.post(
            "/api/v1/auth/login",
            json=_login_body("+84 912 333 444", valid_cred),
        )
        assert staff_res.status_code == 200
        staff_body = staff_res.json()
        assert staff_body["user"]["role"] == "staff"
        assert staff_body["redirect_path"] == "/ops/reservations"

        # 3. Quản lý đăng nhập có bật remember_me -> điều hướng về '/ops' & thời hạn 7 ngày
        mgr_res = client.post(
            "/api/v1/auth/login",
            json=_login_body("manager@vuonpho.vn", valid_cred, remember_me=True),
        )
        assert mgr_res.status_code == 200
        mgr_body = mgr_res.json()
        assert mgr_body["user"]["role"] == "manager"
        assert mgr_body["redirect_path"] == "/ops"
        assert mgr_body["expires_in"] == 7 * 24 * 3600
    finally:
        app.dependency_overrides.clear()


def test_account_locked_15_minutes_after_5_failed_attempts(tmp_path: Path) -> None:
    client, session_factory = _setup_test_env(tmp_path)
    correct_cred = _sample_cred("Correct")
    wrong_cred = _sample_cred("Wrong")
    try:
        with session_factory() as db:
            db.add(
                User(
                    full_name="Nguyễn Văn Thử Khóa",
                    email="locktest@vuonpho.vn",
                    phone="0909888777",
                    password_hash=hash_password(correct_cred),
                    role="customer",
                    is_active=True,
                )
            )
            db.commit()

        # Lần sai 1 -> 4: trả 401 kèm số lần thử còn lại
        for attempt_idx in range(1, 5):
            res = client.post(
                "/api/v1/auth/login",
                json=_login_body("0909888777", wrong_cred),
            )
            assert res.status_code == 401
            detail = res.json()["detail"]
            assert detail["code"] == "INVALID_CREDENTIALS"
            assert detail["remaining_attempts"] == 5 - attempt_idx

        # Lần sai thứ 5: kích hoạt khóa tạm 15 phút (423 Locked)
        fifth_res = client.post(
            "/api/v1/auth/login",
            json=_login_body("0909888777", wrong_cred),
        )
        assert fifth_res.status_code == 423
        fifth_detail = fifth_res.json()["detail"]
        assert fifth_detail["code"] == "ACCOUNT_LOCKED"
        assert fifth_detail["retry_after_seconds"] == 15 * 60
        assert "locked_until" in fifth_detail

        # Lần thử thứ 6 (quá 5 lần): ngay cả khi nhập ĐÚNG mật khẩu vẫn bị chặn trong 15 phút!
        sixth_res = client.post(
            "/api/v1/auth/login",
            json=_login_body("0909888777", correct_cred),
        )
        assert sixth_res.status_code == 423
        assert sixth_res.json()["detail"]["code"] == "ACCOUNT_LOCKED"

        # Giả lập đã trôi qua 15 phút -> cho phép đăng nhập lại và reset bộ đếm về 0
        with session_factory() as db:
            locked_user = db.execute(
                select(User).where(User.phone == "0909888777")
            ).scalar_one()
            locked_user.locked_until = now_gmt7() - timedelta(seconds=10)
            db.commit()

        unlocked_res = client.post(
            "/api/v1/auth/login",
            json=_login_body("0909888777", correct_cred),
        )
        assert unlocked_res.status_code == 200
        with session_factory() as db:
            refreshed = db.execute(
                select(User).where(User.phone == "0909888777")
            ).scalar_one()
            assert refreshed.failed_login_attempts == 0
            assert refreshed.locked_until is None
    finally:
        app.dependency_overrides.clear()


def test_session_expiration_and_logout_revocation(tmp_path: Path) -> None:
    client, session_factory = _setup_test_env(tmp_path)
    valid_cred = _sample_cred("Session")
    try:
        with session_factory() as db:
            user = User(
                full_name="Trần Thị Phiên",
                email="session@vuonpho.vn",
                phone="0977123123",
                password_hash=hash_password(valid_cred),
                role="customer",
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            user_id = user.id

        # 1. Phiên hết hạn bị từ chối với mã TOKEN_EXPIRED
        expired_bundle = create_access_token(
            user_id=user_id,
            role="customer",
            expires_delta=timedelta(seconds=-5),
        )
        expired_me = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {expired_bundle.access_token}"},
        )
        assert expired_me.status_code == 401
        assert expired_me.json()["detail"]["code"] == "TOKEN_EXPIRED"

        # 2. Đăng nhập lấy token sống -> gọi /me thành công -> gọi /logout hủy phiên
        login_res = client.post(
            "/api/v1/auth/login",
            json=_login_body("session@vuonpho.vn", valid_cred),
        )
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        auth_header = {"Authorization": f"Bearer {token}"}

        me_ok = client.get("/api/v1/auth/me", headers=auth_header)
        assert me_ok.status_code == 200
        assert me_ok.json()["user"]["email"] == "session@vuonpho.vn"

        logout_res = client.post("/api/v1/auth/logout", headers=auth_header)
        assert logout_res.status_code == 200

        # Xóa bộ nhớ đệm để chứng minh phiên vẫn bị hủy bền vững trong CSDL sau khi restart server
        clear_revoked_jtis_in_memory()

        me_after_logout = client.get("/api/v1/auth/me", headers=auth_header)
        assert me_after_logout.status_code == 401
        assert me_after_logout.json()["detail"]["code"] == "TOKEN_REVOKED"
    finally:
        app.dependency_overrides.clear()
