"""
Thin wrapper around the Cloudinary SDK for uploading drill/practice videos.
Credentials are read from environment variables only — never hardcoded.
"""
import cloudinary
import cloudinary.uploader

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


def upload_video(file_path_or_stream, folder: str = "athliq/practice_evidence") -> dict:
    """Returns Cloudinary's response dict (contains 'secure_url', 'public_id', etc.)."""
    return cloudinary.uploader.upload(file_path_or_stream, resource_type="video", folder=folder)
