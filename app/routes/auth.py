from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, SessionInfo, TokenResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    email = payload.email.lower()

    existing = db.scalar(select(User).where(User.email == email))

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        email=email,
        name=payload.name.strip(),
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
    )

    return response


@router.post("/token")
def token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.email == username.lower())
    )

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(user.id)

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
    )

    return response


@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.email == payload.email.lower())
    )

    if not user or not verify_password(
        password=payload.password,
        password_hash=user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(user.id)

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
    )

    return response


@router.post("/logout")
def logout():
    response = RedirectResponse(
        url="/",
        status_code=303,
    )

    response.delete_cookie("access_token")

    return response


@router.get("/session-info", response_model=SessionInfo)
def session_info(
    user: User = Depends(get_current_user),
):
    return SessionInfo(
        authenticated=True,
        user_id=user.id,
        name=user.name,
        email=user.email,
    )


@router.get("/session-data")
def session_data(
    user: User = Depends(get_current_user),
):
    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "recommendation_count": len(user.recommendations),
    }