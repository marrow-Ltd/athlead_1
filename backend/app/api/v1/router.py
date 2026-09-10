from fastapi import APIRouter

from app.api.v1.endpoints import ai, auth, coach, drills, practice_evidence, progress, skills, sports, training

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(sports.router)
api_router.include_router(skills.router)
api_router.include_router(drills.router)
api_router.include_router(training.router)
api_router.include_router(progress.router)
api_router.include_router(coach.router)
api_router.include_router(practice_evidence.router)
api_router.include_router(ai.router)
