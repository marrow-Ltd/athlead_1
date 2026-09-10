from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.deps import get_current_user
from app.core.google_auth import verify_google_id_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import GoogleAuthRequest, Token, UserLogin, UserRead, UserRegister
from app.services.auth_service import (
    authenticate_or_create_google_user,
    authenticate_user,
    issue_token_for_user,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, payload)
    token = issue_token_for_user(user)
    return Token(access_token=token, user=UserRead.model_validate(user))


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload)
    token = issue_token_for_user(user)
    return Token(access_token=token, user=UserRead.model_validate(user))


@router.post("/google", response_model=Token)
def google_login(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Verifies the Google-issued ID token (never trusts a client-supplied
    email/name directly), then finds-or-creates the local user account.
    `payload.role` is only used the first time this Google account signs in.
    """
    profile = verify_google_id_token(payload.id_token)  # raises 401 if invalid
    user = authenticate_or_create_google_user(db, profile, payload.role)
    token = issue_token_for_user(user)
    return Token(access_token=token, user=UserRead.model_validate(user))


@router.post("/logout")
def logout(_: User = Depends(get_current_user)):
    # Stateless JWT: logout is handled client-side by discarding the token.
    # (A denylist/refresh-token table can be added later if needed.)
    return {"detail": "Logged out."}


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user