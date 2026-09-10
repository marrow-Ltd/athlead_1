"""
Shared FastAPI dependencies: DB session passthrough, current-user
resolution from JWT, and role guards.

SECURITY NOTE: the authenticated user's identity always comes from the
verified JWT — never from a client-supplied header/body field like
`coach_id`. Every endpoint that needs "the current coach" or
"the current student" must resolve it via these dependencies, not from
request input.
"""
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception

    user = db.get(User, uuid.UUID(payload["sub"]))
    if user is None:
        raise credentials_exception
    return user


def require_role(*allowed_roles: UserRole):
    def _checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return user

    return _checker


require_coach = require_role(UserRole.coach, UserRole.admin)
require_student = require_role(UserRole.student, UserRole.admin)


# Optional-auth variant: used by endpoints that behave differently for
# logged-out vs logged-in users (e.g. GET /api/sports/search) but must not
# reject anonymous requests outright.
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user_optional(
    token: str | None = Depends(optional_oauth2_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    if not token:
        return None
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        return None
    return db.get(User, uuid.UUID(payload["sub"]))
