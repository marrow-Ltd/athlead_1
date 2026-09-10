from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select

from app.core.deps import require_coach
from app.db.session import get_db
from app.models.coach_student import CoachStudent, CoachStudentStatus
from app.models.user import User, UserRole
from app.schemas.coach import AddStudentRequest, CoachStudentRead, CsvUploadResult
from app.services.csv_import_service import import_coach_csv

router = APIRouter(prefix="/coach", tags=["coach"])


@router.get("/students", response_model=list[CoachStudentRead])
def list_my_students(db: Session = Depends(get_db), coach: User = Depends(require_coach)):
    # coach.id comes from the verified JWT, never from a query param.
    return db.exec(select(CoachStudent).where(CoachStudent.coach_id == coach.id)).all()


@router.post("/students", response_model=CoachStudentRead)
def add_student(
    payload: AddStudentRequest,
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach),
):
    student = db.exec(
        select(User).where(User.email == payload.student_email, User.role == UserRole.student)
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="No student found with that email.")

    existing = db.exec(
        select(CoachStudent).where(CoachStudent.coach_id == coach.id, CoachStudent.student_id == student.id)
    ).first()
    if existing:
        return existing

    link = CoachStudent(coach_id=coach.id, student_id=student.id, status=CoachStudentStatus.active)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.get("/students/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db), coach: User = Depends(require_coach)):
    # Ensure the requested student actually belongs to THIS coach.
    link = db.exec(
        select(CoachStudent).where(CoachStudent.coach_id == coach.id, CoachStudent.student_id == student_id)
    ).first()
    if not link:
        raise HTTPException(status_code=404, detail="Student not found for this coach.")
    student = db.get(User, student_id)
    return student


@router.post("/upload-csv", response_model=CsvUploadResult)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    coach: User = Depends(require_coach),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")
    raw = await file.read()
    return import_coach_csv(db, coach, raw)
