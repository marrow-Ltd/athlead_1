import uuid
from datetime import datetime

from pydantic import BaseModel


class SportRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    image_url: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class SportSearchResult(BaseModel):
    """Wraps sport search results with a tag indicating data tier,
    so the frontend can visually distinguish system vs coach-custom data."""
    sport: SportRead
    source: str  # "system" | "coach_custom"
