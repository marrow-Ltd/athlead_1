from dataclasses import dataclass
from fastapi import HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from app.core.config import settings

_google_request = google_requests.Request()

@dataclass
class GoogleProfile:
    google_id: str
    email: str
    email_verified: bool
    name: str

def verify_google_id_token(token: str) -> GoogleProfile:
    if not settings.google_client_id:
        raise HTTPException(500, "Google Sign-In not configured (GOOGLE_CLIENT_ID missing).")
    try:
        claims = google_id_token.verify_oauth2_token(token, _google_request, audience=settings.google_client_id)
    except ValueError:
        raise HTTPException(401, "Invalid or expired Google token.")
    if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise HTTPException(401, "Invalid token issuer.")
    if not claims.get("email_verified", False):
        raise HTTPException(401, "Google email is not verified.")
    return GoogleProfile(
        google_id=claims["sub"], email=claims["email"],
        email_verified=True, name=claims.get("name", claims["email"].split("@")[0]),
    )