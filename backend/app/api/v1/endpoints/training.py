from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.training_assignment import TrainingAssignment
from app.models.training_plan import TrainingPlan
from app.models.user import User
from app.schemas.training import TrainingAssignmentRead, TrainingAssignmentUpdate, TrainingPlanRead

router = APIRouter(prefix="/training", tags=["training"])


@router.get("/plans", response_model=list[TrainingPlanRead])
def list_my_plans(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.exec(select(TrainingPlan).where(TrainingPlan.student_id == current_user.id)).all()


@router.post("/plans", response_model=TrainingPlanRead)
def create_plan(payload: TrainingPlanRead, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # NOTE: student_id is forced to the authenticated user, never trusted from payload.
    plan = TrainingPlan(
        student_id=current_user.id,
        sport_id=payload.sport_id,
        source_type=payload.source_type,
        title=payload.title,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/today", response_model=list[TrainingAssignmentRead])
def training_today(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from datetime import date

    stmt = select(TrainingAssignment).where(
        TrainingAssignment.student_id == current_user.id,
        TrainingAssignment.scheduled_date == date.today(),
    )
    return db.exec(stmt).all()


@router.patch("/assignments/{assignment_id}", response_model=TrainingAssignmentRead)
def update_assignment(
    assignment_id: str,
    payload: TrainingAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = db.get(TrainingAssignment, assignment_id)
    if not assignment or assignment.student_id != current_user.id:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    if payload.status is not None:
        assignment.status = payload.status
    if payload.notes is not None:
        assignment.notes = payload.notes
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
