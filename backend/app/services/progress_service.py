"""Progress-tracking helpers (foundation stub)."""
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models.student_skill_progress import StudentSkillProgress


def record_practice(db: Session, student_id, skill_id, delta: float = 0.05) -> StudentSkillProgress:
    row = db.exec(
        select(StudentSkillProgress).where(
            StudentSkillProgress.student_id == student_id,
            StudentSkillProgress.skill_id == skill_id,
        )
    ).first()
    if not row:
        row = StudentSkillProgress(student_id=student_id, skill_id=skill_id, mastery_score=0.0)

    row.mastery_score = min(1.0, row.mastery_score + delta)
    row.last_practiced_at = datetime.now(timezone.utc)
    row.updated_at = datetime.now(timezone.utc)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
