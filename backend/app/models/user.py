"""User model — students, coaches, and admins all share this table (role-based).
password_hash is optional because Google-authenticated users never set a
local password; google_id is set only for accounts created/linked via
Google Sign-In."""
import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    student = "student"
    coach = "coach"
    admin = "admin"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    password_hash: str | None = Field(default=None)
    google_id: str | None = Field(default=None, unique=True, index=True)
    role: UserRole = Field(default=UserRole.student, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))