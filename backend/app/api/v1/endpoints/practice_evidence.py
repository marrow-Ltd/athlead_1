from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.practice_evidence import PracticeEvidence
from app.models.training_assignment import TrainingAssignment
from app.models.user import User
from app.schemas.practice_evidence import PracticeEvidenceCreate, PracticeEvidenceRead

router = APIRouter(prefix="/practice", tags=["practice-evidence"])


@router.post("/evidence", response_model=PracticeEvidenceRead)
def submit_evidence(
    payload: PracticeEvidenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assignment = db.get(TrainingAssignment, payload.training_assignment_id)
    if not assignment or assignment.student_id != current_user.id:
        raise HTTPException(status_code=404, detail="Training assignment not found.")

    evidence = PracticeEvidence(
        student_id=current_user.id,
        training_assignment_id=payload.training_assignment_id,
        video_url=payload.video_url,
        cloudinary_public_id=payload.cloudinary_public_id,
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    return evidence


@router.get("/evidence", response_model=list[PracticeEvidenceRead])
def list_my_evidence(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.exec(select(PracticeEvidence).where(PracticeEvidence.student_id == current_user.id)).all()
