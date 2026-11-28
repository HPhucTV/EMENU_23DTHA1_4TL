"""REST API Xác thực tài khoản: Đăng ký, Xác thực Email, Đăng nhập & Đăng xuất (FR-01)."""

from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import AuthenticatedSession, get_current_auth_session
from app.schemas.auth_schemas import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
    ResendVerificationRequest,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from app.services.auth_service import (
    DuplicateAccountError,
    LoginAuthenticationError,
    VerificationTokenError,
    authenticate_user,
    build_current_user_response,
    register_customer,
    resend_verification_email,
    revoke_user_session,
    verify_customer_email,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản khách hàng mới và gửi email xác thực",
)
def register_endpoint(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
) -> RegisterResponse | JSONResponse:
    try:
        return register_customer(db=db, payload=payload)
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


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Đăng nhập bằng Email hoặc SĐT, điều hướng theo vai trò và khóa tạm 15p sau 5 lần sai",
)
def login_endpoint(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse | JSONResponse:
    try:
        return authenticate_user(db=db, payload=payload)
    except LoginAuthenticationError as exc:
        detail_payload: dict[str, Any] = {
            "code": exc.code,
            "message": exc.message,
        }
        if exc.locked_until is not None:
            detail_payload["locked_until"] = exc.locked_until.isoformat()
        if exc.retry_after_seconds is not None:
            detail_payload["retry_after_seconds"] = exc.retry_after_seconds
        if exc.remaining_attempts is not None:
            detail_payload["remaining_attempts"] = exc.remaining_attempts
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": detail_payload},
        )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    summary="Lấy thông tin người dùng của phiên đăng nhập hiện hành",
)
def get_me_endpoint(
    auth_session: AuthenticatedSession = Depends(get_current_auth_session),
) -> CurrentUserResponse:
    return build_current_user_response(
        user=auth_session.user, token_data=auth_session.token_data
    )


@router.post(
    "/logout",
    response_model=LogoutResponse,
    summary="Đăng xuất và hủy hiệu lực phiên JWT hiện hành",
)
def logout_endpoint(
    auth_session: AuthenticatedSession = Depends(get_current_auth_session),
    db: Session = Depends(get_db),
) -> LogoutResponse:
    return revoke_user_session(
        db=db, user=auth_session.user, token_data=auth_session.token_data
    )


@router.post(
    "/verify-email",
    response_model=VerifyEmailResponse,
    summary="Xác thực địa chỉ email bằng token một lần gửi trong email",
)
def verify_email_endpoint(
    payload: VerifyEmailRequest,
    db: Session = Depends(get_db),
) -> VerifyEmailResponse | JSONResponse:
    try:
        return verify_customer_email(db=db, raw_token=payload.token)
    except VerificationTokenError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": {
                    "code": "INVALID_VERIFICATION_TOKEN",
                    "message": exc.message,
                }
            },
        )


@router.post(
    "/resend-verification",
    response_model=VerifyEmailResponse,
    summary="Gửi lại email xác thực cho tài khoản chưa kích hoạt email",
)
def resend_verification_endpoint(
    payload: ResendVerificationRequest,
    db: Session = Depends(get_db),
) -> VerifyEmailResponse | JSONResponse:
    try:
        return resend_verification_email(db=db, email=payload.email)
    except VerificationTokenError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": {
                    "code": "VERIFICATION_RESEND_FAILED",
                    "message": exc.message,
                }
            },
        )
