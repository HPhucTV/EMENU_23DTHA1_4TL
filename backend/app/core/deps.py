"""FastAPI dependencies xác thực phiên JWT và phân quyền RBAC 3 vai trò (US-05, US-07)."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    DecodedAccessToken,
    TokenAuthenticationError,
    decode_access_token,
    is_jti_revoked_in_memory,
    mark_jti_revoked_in_memory,
)
from app.models.core_models import ReservationAuditLog, User

UserRole = Literal["customer", "staff", "manager"]
VALID_USER_ROLES: tuple[UserRole, ...] = ("customer", "staff", "manager")

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class AuthenticatedSession:
    user: User
    token_data: DecodedAccessToken


def _is_token_revoked(db: Session, user_id: int, jti: str, expires_at) -> bool:
    if is_jti_revoked_in_memory(jti):
        return True

    revoked_log = db.execute(
        select(ReservationAuditLog.id).where(
            ReservationAuditLog.actor_id == user_id,
            ReservationAuditLog.action == "auth_logout",
            ReservationAuditLog.reason == jti,
        )
    ).scalar_one_or_none()

    if revoked_log is not None:
        mark_jti_revoked_in_memory(jti, expires_at)
        return True
    return False


def get_current_auth_session(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AuthenticatedSession:
    """Xác thực Bearer JWT, kiểm tra hạn phiên, trạng thái hủy phiên và tài khoản hoạt động."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "NOT_AUTHENTICATED",
                "message": "Vui lòng đăng nhập để tiếp tục.",
            },
        )

    try:
        decoded = decode_access_token(credentials.credentials)
    except TokenAuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": exc.code, "message": exc.message},
        ) from exc

    if _is_token_revoked(db, decoded.user_id, decoded.jti, decoded.expires_at):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "TOKEN_REVOKED",
                "message": "Phiên đăng nhập đã được đăng xuất. Vui lòng đăng nhập lại.",
            },
        )

    user = db.get(User, decoded.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "USER_NOT_FOUND",
                "message": "Không tìm thấy tài khoản của phiên đăng nhập này.",
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "ACCOUNT_INACTIVE",
                "message": "Tài khoản đã bị khóa hoạt động. Vui lòng liên hệ Quản lý.",
            },
        )

    return AuthenticatedSession(user=user, token_data=decoded)


def get_current_user(
    session: AuthenticatedSession = Depends(get_current_auth_session),
) -> User:
    return session.user


def require_roles(*allowed_roles: UserRole) -> Callable[..., User]:
    """Dependency kiểm tra vai trò RBAC ở tầng API: ngoài quyền trả 403 và ghi nhật ký."""
    allowed_set = tuple(allowed_roles)

    def _role_checker(
        request: Request,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        if current_user.role not in allowed_set:
            db.add(
                ReservationAuditLog(
                    actor_id=current_user.id,
                    action="rbac_access_denied",
                    old_value={"user_role": current_user.role},
                    new_value={
                        "method": request.method,
                        "path": request.url.path,
                        "allowed_roles": list(allowed_set),
                    },
                    reason=(
                        f"Truy cập ngoài quyền: vai trò '{current_user.role}' "
                        f"cố truy cập {request.method} {request.url.path}"
                    ),
                )
            )
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "FORBIDDEN",
                    "message": "Bạn không có quyền thực hiện chức năng này.",
                    "required_roles": list(allowed_set),
                    "current_role": current_user.role,
                },
            )
        return current_user

    return _role_checker


require_customer = require_roles("customer")
require_staff_or_manager = require_roles("staff", "manager")
require_manager = require_roles("manager")
