"""
Handles the coach CSV-upload workflow end to end:
parse -> validate -> normalize -> map into relational tables.

CSV is treated purely as an INPUT FORMAT — rows are mapped onto Sport /
Skill(implicit) / Drill / TrainingAssignment records, never stored
verbatim as "the" data model (see CoachCustomData for raw-payload
bookkeeping only).
"""
import uuid

from sqlmodel import Session, select

from app.models.drill import Drill
from app.models.sport import Sport
from app.models.training_assignment import TrainingAssignment
from app.models.training_plan import TrainingPlan, TrainingPlanSourceType
from app.models.user import User, UserRole
from app.schemas.coach import CsvUploadResult, CsvUploadRowError
from app.utils.csv_parser import REQUIRED_FIELDS, parse_csv_bytes
from app.utils.validators import is_positive_int, is_valid_email


def _get_or_create_sport(db: Session, sport_name: str) -> Sport:
    sport = db.exec(select(Sport).where(Sport.name == sport_name)).first()
    if sport:
        return sport
    sport = Sport(name=sport_name)
    db.add(sport)
    db.flush()  # get sport.id without committing yet
    return sport


def _get_or_create_plan(db: Session, student_id: uuid.UUID, sport_id: uuid.UUID, coach_id: uuid.UUID) -> TrainingPlan:
    plan = db.exec(
        select(TrainingPlan).where(
            TrainingPlan.student_id == student_id,
            TrainingPlan.sport_id == sport_id,
            TrainingPlan.source_type == TrainingPlanSourceType.coach,
        )
    ).first()
    if plan:
        return plan
    plan = TrainingPlan(
        student_id=student_id,
        sport_id=sport_id,
        created_by=coach_id,
        source_type=TrainingPlanSourceType.coach,
        title=f"Coach plan",
    )
    db.add(plan)
    db.flush()
    return plan


def import_coach_csv(db: Session, coach: User, raw_csv: bytes) -> CsvUploadResult:
    rows = parse_csv_bytes(raw_csv)
    row_errors: list[CsvUploadRowError] = []
    inserted = 0
    updated = 0

    for idx, row in enumerate(rows, start=1):
        errors: list[str] = []

        for field in REQUIRED_FIELDS:
            if not row.get(field):
                errors.append(f"Missing required field '{field}'")

        student_email = row.get("student_email", "").strip()
        if student_email and not is_valid_email(student_email):
            errors.append("Invalid student_email format")

        if row.get("sets") and not is_positive_int(row["sets"]):
            errors.append("'sets' must be a positive integer")
        if row.get("reps") and not is_positive_int(row["reps"]):
            errors.append("'reps' must be a positive integer")
        if row.get("day_number") and not is_positive_int(row["day_number"]):
            errors.append("'day_number' must be a positive integer")

        if errors:
            row_errors.append(CsvUploadRowError(row_number=idx, errors=errors))
            continue

        # Resolve the student — never trust a client-supplied student id,
        # only ever a verified email lookup scoped to role=student.
        student = db.exec(
            select(User).where(User.email == student_email, User.role == UserRole.student)
        ).first()
        if not student:
            row_errors.append(
                CsvUploadRowError(row_number=idx, errors=[f"No student found with email '{student_email}'"])
            )
            continue

        sport = _get_or_create_sport(db, row["sport_name"].strip())

        # Coach-owned custom drill. is_custom + created_by_coach_id are always
        # derived server-side from the authenticated coach, never from the CSV.
        drill = Drill(
            sport_id=sport.id,
            drill_name=row["drill_name"].strip(),
            skill_level=row.get("skill_level", "").strip() or None,
            sets=int(row["sets"]),
            reps=int(row["reps"]),
            video_url=row.get("video_url", "").strip() or None,
            is_custom=True,
            created_by_coach_id=coach.id,
        )
        db.add(drill)
        db.flush()

        plan = _get_or_create_plan(db, student.id, sport.id, coach.id)

        assignment = TrainingAssignment(
            training_plan_id=plan.id,
            student_id=student.id,
            day_number=int(row["day_number"]),
            drill_id=drill.id,
            sets=int(row["sets"]),
            reps=int(row["reps"]),
        )
        db.add(assignment)
        inserted += 1

    db.commit()

    return CsvUploadResult(
        total_rows=len(rows),
        inserted=inserted,
        updated=updated,
        failed=len(row_errors),
        row_errors=row_errors,
    )
