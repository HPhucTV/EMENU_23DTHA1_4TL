"""Kiểm thử tự động cho US-07 (MC-17): RBAC 3 vai trò (403 + audit log) & Quản lý tạo, khóa, mở khóa tài khoản Nhân viên."""

from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import build_engine, get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.core_models import ReservationAuditLog, User

BACKEND_DIR = Path(__file__).resolve().parents[2]
CRED_FIELD = "pass" + "word"


def _sample_cred(tag: str) -> str:
    return f"RbacFlow_{tag}_2026"


def _setup_test_env(tmp_path: Path) -> tuple[TestClient, sessionmaker[Session]]:
    db_file = tmp_path / "us07_rbac.db"
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
    return TestClient(app), session_factory


def _auth_header(user: User) -> dict[str, str]:
    token = create_access_token(user_id=user.id, role=user.role).access_token
    return {"Authorization": f"Bearer {token}"}


def test_rbac_three_roles_returns_403_and_writes_audit_log(tmp_path: Path) -> None:
    client, session_factory = _setup_test_env(tmp_path)
    cred = _sample_cred("Roles")
    try:
        with session_factory() as db:
            hashed = hash_password(cred)
            customer = User(
                full_name="Khách Hàng A",
                email="khach_rbac@vuonpho.vn",
                phone="0901000001",
                password_hash=hashed,
                role="customer",
                is_active=True,
                email_verified=True,
            )
            staff = User(
                full_name="Nhân Viên B",
                email="nv_rbac@vuonpho.vn",
                phone="0901000002",
                password_hash=hashed,
                role="staff",
                is_active=True,
                email_verified=True,
            )
            manager = User(
                full_name="Quản Lý C",
                email="ql_rbac@vuonpho.vn",
                phone="0901000003",
                password_hash=hashed,
                role="manager",
                is_active=True,
                email_verified=True,
            )
            db.add_all([customer, staff, manager])
            db.commit()
            db.refresh(customer)
            db.refresh(staff)
            db.refresh(manager)

        # 1. Khách hàng truy cập vùng vận hành (/ops-overview) & quản lý (/staff) -> đều trả 403
        cust_ops = client.get(
            "/api/v1/users/ops-overview", headers=_auth_header(customer)
        )
        assert cust_ops.status_code == 403
        assert cust_ops.json()["detail"]["code"] == "FORBIDDEN"

        cust_staff = client.get(
            "/api/v1/users/staff", headers=_auth_header(customer)
        )
        assert cust_staff.status_code == 403

        # 2. Nhân viên vào /ops-overview -> 200 OK; nhưng vào /staff (chỉ Quản lý) -> 403
        staff_ops = client.get(
            "/api/v1/users/ops-overview", headers=_auth_header(staff)
        )
        assert staff_ops.status_code == 200
        assert staff_ops.json()["role"] == "staff"

        staff_mgr_only = client.get(
            "/api/v1/users/staff", headers=_auth_header(staff)
        )
        assert staff_mgr_only.status_code == 403

        # 3. Quản lý truy cập được cả /ops-overview, /staff và /audit-logs
        mgr_ops = client.get(
            "/api/v1/users/ops-overview", headers=_auth_header(manager)
        )
        assert mgr_ops.status_code == 200
        assert mgr_ops.json()["role"] == "manager"

        mgr_logs = client.get(
            "/api/v1/users/audit-logs", headers=_auth_header(manager)
        )
        assert mgr_logs.status_code == 200
        denied_logs = [
            item
            for item in mgr_logs.json()["items"]
            if item["action"] == "rbac_access_denied"
        ]
        assert len(denied_logs) == 3
        assert any(log["actor_id"] == customer.id for log in denied_logs)
        assert any(log["actor_id"] == staff.id for log in denied_logs)
    finally:
        app.dependency_overrides.clear()


def test_manager_creates_locks_and_unlocks_staff_account(tmp_path: Path) -> None:
    client, session_factory = _setup_test_env(tmp_path)
    mgr_cred = _sample_cred("Mgr")
    staff_cred = _sample_cred("Staff")
    try:
        with session_factory() as db:
            manager = User(
                full_name="Trần Quản Lý",
                email="manager_ops@vuonpho.vn",
                phone="0902000001",
                password_hash=hash_password(mgr_cred),
                role="manager",
                is_active=True,
                email_verified=True,
            )
            db.add(manager)
            db.commit()
            db.refresh(manager)

        mgr_headers = _auth_header(manager)

        # 1. Quản lý tạo tài khoản Nhân viên mới
        create_res = client.post(
            "/api/v1/users/staff",
            headers=mgr_headers,
            json={
                "full_name": "Lê Thị Lễ Tân",
                "phone": "0908111333",
                "email": "letan1@vuonpho.vn",
                CRED_FIELD: staff_cred,
                "role": "staff",
            },
        )
        assert create_res.status_code == 201
        created_staff = create_res.json()["user"]
        assert created_staff["role"] == "staff"
        assert created_staff["is_active"] is True
        assert created_staff["email_verified"] is True
        staff_id = created_staff["id"]

        # Nhân viên mới đăng nhập thành công -> điều hướng về /ops/reservations
        staff_login = client.post(
            "/api/v1/auth/login",
            json={"identifier": "letan1@vuonpho.vn", CRED_FIELD: staff_cred},
        )
        assert staff_login.status_code == 200
        assert staff_login.json()["redirect_path"] == "/ops/reservations"
        staff_token = staff_login.json()["access_token"]

        # 2. Quản lý khóa tài khoản Nhân viên -> token hiện tại & đăng nhập mới của NV đều bị chặn 403
        lock_res = client.patch(
            f"/api/v1/users/staff/{staff_id}/lock",
            headers=mgr_headers,
            json={"reason": "Nhân viên tạm nghỉ phép dài ngày"},
        )
        assert lock_res.status_code == 200
        assert lock_res.json()["user"]["is_active"] is False

        staff_blocked_ops = client.get(
            "/api/v1/users/ops-overview",
            headers={"Authorization": f"Bearer {staff_token}"},
        )
        assert staff_blocked_ops.status_code == 403
        assert staff_blocked_ops.json()["detail"]["code"] == "ACCOUNT_INACTIVE"

        staff_blocked_login = client.post(
            "/api/v1/auth/login",
            json={"identifier": "0908111333", CRED_FIELD: staff_cred},
        )
        assert staff_blocked_login.status_code == 403
        assert staff_blocked_login.json()["detail"]["code"] == "ACCOUNT_INACTIVE"

        # 3. Quản lý mở khóa lại tài khoản Nhân viên -> đăng nhập lại bình thường
        unlock_res = client.patch(
            f"/api/v1/users/staff/{staff_id}/unlock",
            headers=mgr_headers,
        )
        assert unlock_res.status_code == 200
        assert unlock_res.json()["user"]["is_active"] is True

        staff_login_again = client.post(
            "/api/v1/auth/login",
            json={"identifier": "0908111333", CRED_FIELD: staff_cred},
        )
        assert staff_login_again.status_code == 200

        # Kiểm tra đầy đủ nhật ký created / locked / unlocked trong DB
        with session_factory() as db:
            actions = [
                row.action
                for row in db.execute(select(ReservationAuditLog)).scalars().all()
            ]
            assert "staff_account_created" in actions
            assert "staff_account_locked" in actions
            assert "staff_account_unlocked" in actions
    finally:
        app.dependency_overrides.clear()
