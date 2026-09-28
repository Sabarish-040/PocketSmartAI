
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token",
    auto_error=False,
)


def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    bearer_token = token

    if not bearer_token:
        bearer_token = request.cookies.get("access_token")

    if not bearer_token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    bearer_token = bearer_token.replace("Bearer ", "")

    user_id = decode_access_token(bearer_token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user