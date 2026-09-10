import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.coach_student import CoachStudentStatus


class CoachStudentRead(BaseModel):
    id: uuid.UUID
    coach_id: uuid.UUID
    student_id: uuid.UUID
    status: CoachStudentStatus
    created_at: datetime

    class Config:
        from_attributes = True


class AddStudentRequest(BaseModel):
    student_email: EmailStr


class CsvUploadRowError(BaseModel):
    row_number: int
    errors: list[str]


class CsvUploadResult(BaseModel):
    total_rows: int
    inserted: int
    updated: int
    failed: int
    row_errors: list[CsvUploadRowError]
