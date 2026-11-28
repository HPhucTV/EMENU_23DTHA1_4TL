"""REST API Phân quyền 3 vai trò & Quản lý tài khoản Nhân viên (FR-01 — US-07)."""

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_manager, require_staff_or_manager
from app.models.core_models import User
from app.schemas.user_schemas import (
    AuditLogListResponse,
    LockAccountRequest,
    OpsOverviewResponse,
    StaffAccountActionResponse,
    StaffAccountCreateRequest,
    StaffListResponse,
)
from app.services.auth_service import DuplicateAccountError
from app.services.user_service import (
    StaffManagementError,
    create_staff_account,
    list_security_audit_logs,
    list_staff_accounts,
    set_staff_account_active_status,
)

router = APIRouter(prefix="/users", tags=["Users & RBAC"])


@router.get(
    "/ops-overview",
    response_model=OpsOverviewResponse,
    summary="Điểm kiểm tra quyền truy cập không gian vận hành (chỉ Nhân viên & Quản lý)",
)
def get_ops_overview_endpoint(
    current_user: User = Depends(require_staff_or_manager),
) -> OpsOverviewResponse:
    if current_user.role == "manager":
        modules = [
            "reservations",
            "tables_edit",
            "menu_edit",
            "kitchen",
            "reports",
            "staff_management",
            "configs",
        ]
        role_value = "manager"
    else:
        modules = ["reservations", "tables_view", "menu_stock", "kitchen"]
        role_value = "staff"

    return OpsOverviewResponse(
        message="Xác nhận quyền truy cập không gian vận hành thành công.",
        role=role_value,
        allowed_modules=modules,
    )


@router.get(
    "/staff",
    response_model=StaffListResponse,
    summary="Danh sách tài khoản nhân sự (chỉ Quản lý)",
)
def list_staff_endpoint(
    search: str | None = Query(default=None, description="Tìm theo tên, email, SĐT"),
    status_filter: str | None = Query(
        default=None, description="Lọc theo trạng thái: active | locked"
    ),
    _manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> StaffListResponse:
    return list_staff_accounts(
        db, search=search, status_filter=status_filter
    )


@router.post(
    "/staff",
    response_model=StaffAccountActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Quản lý tạo tài khoản Nhân viên mới",
)
def create_staff_endpoint(
    payload: StaffAccountCreateRequest,
    manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> StaffAccountActionResponse | JSONResponse:
    try:
        return create_staff_account(db, manager=manager, payload=payload)
    except DuplicateAccountError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": {
                    "code": "DUPLICATE_ACCOUNT",
                    "message": exc.message,
                    "field_errors": exc.field_errors,
                }
            },
        )


@router.patch(
    "/staff/{user_id}/lock",
    response_model=StaffAccountActionResponse,
    summary="Quản lý khóa tài khoản Nhân viên",
)
def lock_staff_endpoint(
    user_id: int,
    payload: LockAccountRequest | None = None,
    manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> StaffAccountActionResponse | JSONResponse:
    try:
        return set_staff_account_active_status(
            db,
            manager=manager,
            target_user_id=user_id,
            is_active=False,
            reason=payload.reason if payload else None,
        )
    except StaffManagementError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": {"code": exc.code, "message": exc.message}},
        )


@router.patch(
    "/staff/{user_id}/unlock",
    response_model=StaffAccountActionResponse,
    summary="Quản lý mở khóa tài khoản Nhân viên",
)
def unlock_staff_endpoint(
    user_id: int,
    manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> StaffAccountActionResponse | JSONResponse:
    try:
        return set_staff_account_active_status(
            db,
            manager=manager,
            target_user_id=user_id,
            is_active=True,
        )
    except StaffManagementError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": {"code": exc.code, "message": exc.message}},
        )


@router.get(
    "/audit-logs",
    response_model=AuditLogListResponse,
    summary="Xem nhật ký bảo mật RBAC (403) và quản lý tài khoản (chỉ Quản lý)",
)
def get_security_audit_logs_endpoint(
    limit: int = Query(default=30, ge=1, le=100),
    _manager: User = Depends(require_manager),
    db: Session = Depends(get_db),
) -> AuditLogListResponse:
    return list_security_audit_logs(db, limit=limit)
