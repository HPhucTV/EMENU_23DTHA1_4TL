"""REST API Xác thực tài khoản (FR-01 — US-04: Đăng ký & Xác thực Email)."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth_schemas import (
    RegisterRequest,
    RegisterResponse,
    ResendVerificationRequest,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from app.services.auth_service import (
    DuplicateAccountError,
    VerificationTokenError,
    register_customer,
    resend_verification_email,
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
