"""Business logic for registration/login, kept out of the route handlers."""
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.google_auth import GoogleProfile
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserLogin, UserRegister


def register_user(db: Session, payload: UserRegister) -> User:
    existing = db.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: UserLogin) -> User:
    user = db.exec(select(User).where(User.email == payload.email)).first()
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    return user


def authenticate_or_create_google_user(db: Session, profile: GoogleProfile, requested_role: UserRole) -> User:
    # 1) Already linked by google_id -> just log in.
    user = db.exec(select(User).where(User.google_id == profile.google_id)).first()
    if user:
        return user

    # 2) An account with this email exists (e.g. they registered with a
    #    password earlier) -> link Google to it instead of duplicating.
    user = db.exec(select(User).where(User.email == profile.email)).first()
    if user:
        user.google_id = profile.google_id
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # 3) Brand new account.
    user = User(
        name=profile.name,
        email=profile.email,
        password_hash=None,
        google_id=profile.google_id,
        role=requested_role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def issue_token_for_user(user: User) -> str:
    return create_access_token(subject=str(user.id), extra_claims={"role": user.role.value})