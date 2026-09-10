"""
Implements the two-tier (system vs coach-custom) sport search logic
described in the architecture doc. All authorization checks happen
here (server-side), never trusting client-supplied ids.
"""
import uuid

from sqlmodel import Session, or_, select

from app.models.coach_student import CoachStudent, CoachStudentStatus
from app.models.drill import Drill
from app.models.sport import Sport
from app.models.user import User, UserRole


def search_sports(db: Session, current_user: User | None, query: str | None = None) -> dict:
    """
    Returns a dict with:
      - system: list[Sport]              -> always visible
      - coach_custom_drills: list[Drill] -> only for authenticated users, scoped per role
    """
    sport_stmt = select(Sport)
    if query:
        sport_stmt = sport_stmt.where(Sport.name.ilike(f"%{query}%"))
    system_sports = db.exec(sport_stmt).all()

    coach_custom_drills: list[Drill] = []

    if current_user is None:
        # Unauthenticated: system data only.
        return {"system": system_sports, "coach_custom_drills": []}

    if current_user.role == UserRole.coach:
        # Coach sees their OWN custom drills only.
        drill_stmt = select(Drill).where(
            Drill.is_custom == True,  # noqa: E712
            Drill.created_by_coach_id == current_user.id,
        )
        coach_custom_drills = db.exec(drill_stmt).all()

    elif current_user.role == UserRole.student:
        # Student sees custom drills from coach(es) they are actively linked to.
        coach_link_stmt = select(CoachStudent.coach_id).where(
            CoachStudent.student_id == current_user.id,
            CoachStudent.status == CoachStudentStatus.active,
        )
        coach_ids = db.exec(coach_link_stmt).all()
        if coach_ids:
            drill_stmt = select(Drill).where(
                Drill.is_custom == True,  # noqa: E712
                Drill.created_by_coach_id.in_(coach_ids),
            )
            coach_custom_drills = db.exec(drill_stmt).all()

    return {"system": system_sports, "coach_custom_drills": coach_custom_drills}
