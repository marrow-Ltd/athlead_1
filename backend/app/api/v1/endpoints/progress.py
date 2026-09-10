from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.student_skill_progress import StudentSkillProgress
from app.models.user import User
from app.schemas.progress import StudentSkillProgressRead

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=list[StudentSkillProgressRead])
def my_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.exec(select(StudentSkillProgress).where(StudentSkillProgress.student_id == current_user.id)).all()


@router.get("/skills/{skill_id}", response_model=StudentSkillProgressRead | None)
def my_progress_for_skill(skill_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.exec(
        select(StudentSkillProgress).where(
            StudentSkillProgress.student_id == current_user.id,
            StudentSkillProgress.skill_id == skill_id,
        )
    ).first()
