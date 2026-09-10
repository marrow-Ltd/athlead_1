from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_db
from app.models.drill import Drill
from app.schemas.drill import DrillRead

router = APIRouter(prefix="/drills", tags=["drills"])


@router.get("", response_model=list[DrillRead])
def list_drills(sport_id: str | None = None, skill_id: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Drill).where(Drill.is_custom == False)  # noqa: E712  (system drills only on this public listing)
    if sport_id:
        stmt = stmt.where(Drill.sport_id == sport_id)
    if skill_id:
        stmt = stmt.where(Drill.skill_id == skill_id)
    return db.exec(stmt).all()


@router.get("/search", response_model=list[DrillRead])
def search_drills(q: str, db: Session = Depends(get_db)):
    stmt = select(Drill).where(Drill.drill_name.ilike(f"%{q}%"), Drill.is_custom == False)  # noqa: E712
    return db.exec(stmt).all()


@router.get("/{drill_id}", response_model=DrillRead)
def get_drill(drill_id: str, db: Session = Depends(get_db)):
    drill = db.get(Drill, drill_id)
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found.")
    return drill
