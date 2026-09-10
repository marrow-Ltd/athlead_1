"""
Seam for RAG / next-drill recommendation logic. Consumes the athlete's
structured learning state (StudentSkillProgress, TrainingAssignment
history) rather than acting as an isolated chatbot, per the
architecture doc.
"""
from sqlmodel import Session, select

from app.models.student_skill_progress import StudentSkillProgress


def get_weakest_skills(db: Session, student_id, limit: int = 3) -> list[StudentSkillProgress]:
    stmt = (
        select(StudentSkillProgress)
        .where(StudentSkillProgress.student_id == student_id)
        .order_by(StudentSkillProgress.mastery_score.asc())
        .limit(limit)
    )
    return db.exec(stmt).all()
