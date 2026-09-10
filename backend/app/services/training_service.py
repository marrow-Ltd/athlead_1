"""Plan generation / day scheduling business logic (foundation stub)."""
from sqlmodel import Session

from app.models.training_plan import TrainingPlan, TrainingPlanSourceType


def create_system_starter_plan(db: Session, student_id, sport_id, title: str = "Starter Plan") -> TrainingPlan:
    plan = TrainingPlan(
        student_id=student_id,
        sport_id=sport_id,
        source_type=TrainingPlanSourceType.system,
        title=title,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan
