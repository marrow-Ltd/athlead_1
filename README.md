# AthliQ — Multi-Sport Athlete Learning Platform

A student can train independently (self-learning) or with a coach — both
modes operate on the same persistent **athlete learning state**. See
`docs/APPROACH.md` for the full architecture rationale.

This repo is the **Phase-1 foundation** boilerplate: project structure,
DB models + migration, auth, the tiered sport-search endpoint, and the
coach CSV-upload endpoint — ready to build the rest of the MVP on top of.

## Stack
Next.js + TypeScript + Tailwind · FastAPI + Pydantic + SQLModel ·
PostgreSQL + pgvector · Cloudinary (media)

## Quickstart (local, via Docker Compose)

```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
# edit backend/.env — set a real JWT_SECRET_KEY, DB creds, Cloudinary keys

cd infra
docker compose up --build
```

- Backend: http://localhost:8000 (docs at /docs)
- Frontend: http://localhost:3000
- Postgres (with pgvector): localhost:5432

## Quickstart (without Docker)

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit DATABASE_URL etc.
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## Project layout

```
frontend/   Next.js app (App Router, web)
mobile/     React Native app (Expo Router) — same backend, same endpoints
backend/    FastAPI app
infra/      docker-compose + AWS placeholders
docs/       architecture, schema, and API route reference
```

## Mobile app (React Native / Expo)

```bash
cd mobile
npm install
cp .env.example .env   # set EXPO_PUBLIC_API_BASE_URL to your machine's LAN IP
npx expo start
```

See `mobile/README.md` for details. It reuses the exact same backend API
as the web frontend — same auth flow, same tiered sports-search/CSV-upload
endpoints — just with AsyncStorage instead of localStorage and React
Native views instead of Tailwind/HTML.

See `docs/APPROACH.md`, `docs/db-schema.md`, and `docs/api-routes.md` for
details, and the "Deliberate deviations" note in APPROACH.md for the one
place this repo departs from the original spec doc (route-group URL
collision fix).

## Security notes baked into this boilerplate
- Passwords are bcrypt-hashed, never stored in plaintext.
- All identity (`coach_id`, `student_id`) is derived from the verified JWT
  server-side — never trusted from client-supplied fields.
- `GET /api/sports/search` and `POST /api/coach/upload-csv` both enforce
  the two-tier (system vs coach-custom) access rules described in
  `docs/APPROACH.md`.
- Secrets live in `.env` files (git-ignored) — see `*.env.example` for the
  required variable names.
