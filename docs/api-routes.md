# API routes (v1)

All routes are mounted under `/api`. Auth uses a Bearer JWT
(`Authorization: Bearer <token>`), obtained from `/api/auth/login`.

## Auth
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET  /api/auth/me

## Sports / Skills / Drills
- GET /api/sports
- GET /api/sports/search        (tiered: anonymous / student / coach)
- GET /api/sports/{sport_id}
- GET /api/sports/{sport_id}/skills
- GET /api/skills/{skill_id}
- GET /api/drills
- GET /api/drills/search
- GET /api/drills/{drill_id}

## Training / Progress
- GET   /api/training/plans
- POST  /api/training/plans
- GET   /api/training/today
- PATCH /api/training/assignments/{assignment_id}
- GET   /api/progress
- GET   /api/progress/skills/{skill_id}

## Coach
- GET  /api/coach/students
- POST /api/coach/students
- GET  /api/coach/students/{student_id}
- POST /api/coach/upload-csv

## Practice evidence
- POST /api/practice/evidence
- GET  /api/practice/evidence

## AI (stubs — see docs/APPROACH.md)
- POST /api/ai/recommendations
- POST /api/ai/training-plan
- GET  /api/ai/drill-search
