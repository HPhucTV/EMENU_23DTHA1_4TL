"""Nghiệp vụ Quản lý tài khoản Nhân viên & Nhật ký RBAC (FR-01 — US-07)."""

from sqlalchemy import desc, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.core_models import ReservationAuditLog, User
from app.schemas.user_schemas import (
    AuditLogListResponse,
    AuditLogRead,
    StaffAccountActionResponse,
    StaffAccountCreateRequest,
    StaffAccountRead,
    StaffListResponse,
)
from app.services.auth_service import DuplicateAccountError


class StaffManagementError(Exception):
    """Ngoại lệ khi thao tác quản lý tài khoản nhân viên không hợp lệ."""

    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def list_staff_accounts(
    db: Session,
    *,
    search: str | None = None,
    status_filter: str | None = None,
) -> StaffListResponse:
    """Lấy danh sách tài khoản nội bộ (staff, manager) kèm bộ đếm trạng thái."""
    all_internal = (
        db.execute(
            select(User)
            .where(User.role.in_(("staff", "manager")))
            .order_by(desc(User.created_at), desc(User.id))
        )
        .scalars()
        .all()
    )

    active_count = sum(1 for u in all_internal if u.is_active)
    locked_count = sum(1 for u in all_internal if not u.is_active)

    filtered = all_internal
    if status_filter == "active":
        filtered = [u for u in filtered if u.is_active]
    elif status_filter == "locked":
        filtered = [u for u in filtered if not u.is_active]

    if search and search.strip():
        kw = search.strip().lower()
        filtered = [
            u
            for u in filtered
            if kw in u.full_name.lower()
            or kw in u.email.lower()
            or kw in u.phone.lower()
        ]

    return StaffListResponse(
        items=[StaffAccountRead.model_validate(u) for u in filtered],
        total=len(filtered),
        active_count=active_count,
        locked_count=locked_count,
    )


def create_staff_account(
    db: Session,
    *,
    manager: User,
    payload: StaffAccountCreateRequest,
) -> StaffAccountActionResponse:
    """Quản lý tạo tài khoản Nhân viên mới (mật khẩu băm bcrypt, ghi audit log)."""
    existing = (
        db.execute(
            select(User).where(
                or_(User.email == payload.email, User.phone == payload.phone)
            )
        )
        .scalars()
        .all()
    )
    if existing:
        field_errors: dict[str, str] = {}
        if any(u.email == payload.email for u in existing):
            field_errors["email"] = "Email này đã được sử dụng cho tài khoản khác."
        if any(u.phone == payload.phone for u in existing):
            field_errors["phone"] = "Số điện thoại này đã được sử dụng cho tài khoản khác."
        raise DuplicateAccountError(
            message=next(iter(field_errors.values())),
            field_errors=field_errors,
        )

    staff_user = User(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role=payload.role,
        is_active=True,
        email_verified=True,
        failed_login_attempts=0,
    )
    db.add(staff_user)

    try:
        db.flush()
        db.add(
            ReservationAuditLog(
                actor_id=manager.id,
                action="staff_account_created",
                new_value={
                    "target_user_id": staff_user.id,
                    "email": staff_user.email,
                    "phone": staff_user.phone,
                    "role": staff_user.role,
                },
                reason=f"Quản lý {manager.full_name} tạo tài khoản {staff_user.role}",
            )
        )
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateAccountError(
            message="Email hoặc số điện thoại vừa bị trùng. Vui lòng kiểm tra lại.",
            field_errors={"email": "Email hoặc số điện thoại có thể đã tồn tại."},
        ) from exc

    db.refresh(staff_user)
    return StaffAccountActionResponse(
        message=f"Đã tạo tài khoản {staff_user.role} cho {staff_user.full_name}.",
        user=StaffAccountRead.model_validate(staff_user),
    )


def set_staff_account_active_status(
    db: Session,
    *,
    manager: User,
    target_user_id: int,
    is_active: bool,
    reason: str | None = None,
) -> StaffAccountActionResponse:
    """Quản lý khóa hoặc mở khóa tài khoản Nhân viên (lưu nhật ký kiểm toán)."""
    target_user = db.get(User, target_user_id)
    if target_user is None:
        raise StaffManagementError(
            code="USER_NOT_FOUND",
            message="Không tìm thấy tài khoản nhân viên này.",
            status_code=404,
        )

    if target_user.id == manager.id and not is_active:
        raise StaffManagementError(
            code="CANNOT_LOCK_SELF",
            message="Không thể tự khóa tài khoản Quản lý đang đăng nhập.",
            status_code=400,
        )

    if target_user.role != "staff":
        raise StaffManagementError(
            code="INVALID_TARGET_ROLE",
            message="Chỉ được phép khóa hoặc mở khóa tài khoản có vai trò Nhân viên (staff).",
            status_code=400,
        )

    if target_user.is_active == is_active:
        state_text = "đang hoạt động" if is_active else "đang bị khóa"
        raise StaffManagementError(
            code="STATE_UNCHANGED",
            message=f"Tài khoản {target_user.full_name} hiện {state_text}.",
            status_code=400,
        )

    old_active = target_user.is_active
    target_user.is_active = is_active
    if is_active:
        target_user.failed_login_attempts = 0
        target_user.locked_until = None

    action_name = "staff_account_unlocked" if is_active else "staff_account_locked"
    default_reason = (
        f"Quản lý {manager.full_name} mở khóa tài khoản nhân viên"
        if is_active
        else f"Quản lý {manager.full_name} khóa tài khoản nhân viên"
    )
    cleaned_reason = reason.strip() if reason and reason.strip() else default_reason

    db.add(
        ReservationAuditLog(
            actor_id=manager.id,
            action=action_name,
            old_value={"target_user_id": target_user.id, "is_active": old_active},
            new_value={"target_user_id": target_user.id, "is_active": is_active},
            reason=cleaned_reason,
        )
    )
    db.commit()
    db.refresh(target_user)

    msg = (
        f"Đã mở khóa tài khoản nhân viên {target_user.full_name}."
        if is_active
        else f"Đã khóa tài khoản nhân viên {target_user.full_name}."
    )
    return StaffAccountActionResponse(
        message=msg,
        user=StaffAccountRead.model_validate(target_user),
    )


def list_security_audit_logs(
    db: Session, *, limit: int = 30
) -> AuditLogListResponse:
    """Trả về nhật ký phân quyền (403) và thay đổi tài khoản nhân viên gần nhất."""
    logs = (
        db.execute(
            select(ReservationAuditLog)
            .where(
                ReservationAuditLog.action.in_(
                    (
                        "rbac_access_denied",
                        "staff_account_created",
                        "staff_account_locked",
                        "staff_account_unlocked",
                        "auth_account_locked",
                    )
                )
            )
            .order_by(desc(ReservationAuditLog.created_at), desc(ReservationAuditLog.id))
            .limit(limit)
        )
        .scalars()
        .all()
    )
    return AuditLogListResponse(
        items=[AuditLogRead.model_validate(item) for item in logs],
        total=len(logs),
    )
