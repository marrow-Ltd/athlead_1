"""Coach-student authorization checks reused across services/endpoints."""
from sqlmodel import Session, select

from app.models.coach_student import CoachStudent, CoachStudentStatus


def coach_owns_student(db: Session, coach_id, student_id) -> bool:
    link = db.exec(
        select(CoachStudent).where(
            CoachStudent.coach_id == coach_id,
            CoachStudent.student_id == student_id,
            CoachStudent.status == CoachStudentStatus.active,
        )
    ).first()
    return link is not None
