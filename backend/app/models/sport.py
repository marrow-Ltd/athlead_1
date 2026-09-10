"""Sports catalog — system-level reference data available to all users."""
import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Sport(SQLModel, table=True):
    __tablename__ = "sports"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str | None = None
    image_url: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
