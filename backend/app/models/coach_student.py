"""
Coach <-> Student relationship. A student keeps a single account/learning
state and can optionally be linked to a coach via this join table.
"""
import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class CoachStudentStatus(str, Enum):
    pending = "pending"
    active = "active"
    revoked = "revoked"


class CoachStudent(SQLModel, table=True):
    __tablename__ = "coach_students"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    coach_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    student_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    status: CoachStudentStatus = Field(default=CoachStudentStatus.pending)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
