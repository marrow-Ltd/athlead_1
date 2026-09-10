from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_current_user_optional
from app.db.session import get_db
from app.models.sport import Sport
from app.models.user import User
from app.schemas.drill import DrillRead
from app.schemas.sport import SportRead
from app.services.sports_service import search_sports

router = APIRouter(prefix="/sports", tags=["sports"])


@router.get("", response_model=list[SportRead])
def list_sports(db: Session = Depends(get_db)):
    return db.exec(select(Sport)).all()


@router.get("/search")
def search(
    q: str | None = None,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    """
    Tiered sport search:
      - Unauthenticated: system data only.
      - Student: system data + custom data from their linked coach(es).
      - Coach: system data + their own custom drills.
    All authorization is resolved server-side from the verified JWT
    (get_current_user_optional) — never from a client-supplied role/id.
    """
    result = search_sports(db, current_user, query=q)
    return {
        "system": [SportRead.model_validate(s) for s in result["system"]],
        "coach_custom_drills": [DrillRead.model_validate(d) for d in result["coach_custom_drills"]],
    }


@router.get("/{sport_id}", response_model=SportRead)
def get_sport(sport_id: str, db: Session = Depends(get_db)):
    sport = db.get(Sport, sport_id)
    if not sport:
        raise HTTPException(status_code=404, detail="Sport not found.")
    return sport
