from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillRead

router = APIRouter(tags=["skills"])


@router.get("/sports/{sport_id}/skills", response_model=list[SkillRead])
def list_skills_for_sport(sport_id: str, db: Session = Depends(get_db)):
    return db.exec(select(Skill).where(Skill.sport_id == sport_id)).all()


@router.get("/skills/{skill_id}", response_model=SkillRead)
def get_skill(skill_id: str, db: Session = Depends(get_db)):
    skill = db.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found.")
    return skill
