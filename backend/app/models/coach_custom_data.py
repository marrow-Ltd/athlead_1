"""
Generic container for coach-uploaded custom data that doesn't map 1:1 onto
another table (kept separate from CSV rows themselves — CSV is just an
import format, see services/csv_import_service.py).
"""
import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class CoachCustomData(SQLModel, table=True):
    __tablename__ = "coach_custom_data"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    coach_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    student_id: uuid.UUID | None = Field(default=None, foreign_key="users.id", index=True)
    data_type: str  # e.g. "csv_import", "note"
    payload: str  # JSON-encoded free-form payload for MVP
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
