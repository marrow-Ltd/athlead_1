from app.core.google_auth import GoogleProfile

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