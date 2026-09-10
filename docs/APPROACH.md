# AthliQ — Architecture Approach (canonical)

This is the canonical architecture document. An earlier MongoDB-based draft
has been superseded — **PostgreSQL + pgvector** is the final decision.

## Stack
- Frontend: Next.js (App Router) + TypeScript + Tailwind
- Backend: FastAPI + Pydantic + SQLModel (SQLAlchemy)
- Database: PostgreSQL + pgvector (single database, no separate vector store)
- Media: Cloudinary (videos), external YouTube URLs supported for tutorials
- Deployment target: AWS (post-MVP)

## Core principle
The **athlete** is the central object. Self-learning and coached learning are
two modes operating on the *same* persistent athlete learning state
(current sport/level/goal, skills, mastery, training plan, assignments,
practice evidence, feedback). A student never restarts their journey when
they later connect with a coach.

## Data tiers
- **Tier 1 — System data**: sports, skills, system drills, system plans.
  Visible to everyone.
- **Tier 2 — Coach custom data**: coach-created drills/plans/CSV imports.
  Private to that coach and their linked students. All access control is
  enforced **server-side** (never trust client-supplied coach/student ids —
  always derive identity from the verified JWT).

## CSV
CSV is an **import format**, not the data model. Rows are parsed, validated,
normalized, and mapped onto Sport / Drill / TrainingAssignment records.

## AI / pgvector
`drill_embeddings` / `skill_embeddings` tables hold vector columns for
semantic search and RAG. AI consumes the structured athlete state — it is
not an isolated chatbot. Advanced video analysis / computer vision is
explicitly out of MVP scope.

## What this repo currently contains (Phase 0 — foundation)
- Full folder layout for frontend + backend
- SQLModel models for the foundational + full MVP entity set
- One hand-written initial Alembic migration (creates all tables +
  enables the `vector` extension)
- FastAPI auth (register/login/me, JWT, bcrypt password hashing)
- `GET /api/sports/search` demonstrating the 3-tier access logic
  (anonymous / student / coach)
- `POST /api/coach/upload-csv` with field validation and per-row error
  reporting
- Pydantic schemas mirrored by hand-written TypeScript types
- Next.js pages wired to the API client for every route in the MVP scope
  (drill/video interface renders a placeholder player — swap in a real
  Cloudinary/YouTube player next)

## Deliberate deviations from the original spec doc
- The original spec's frontend tree nests `dashboard/page.tsx` under
  **both** the `(student)` and `(coach)` route groups. Next.js route
  groups are stripped from the URL, so both would resolve to the same
  `/dashboard` path and fail to build. This repo uses real segments,
  `/student/...` and `/coach/...`, instead — everything else follows the
  spec's tree as written.
- `mobile/` (React Native, added after the initial web build) hits the
  same collision with Expo Router's `(group)` folders, and is fixed the
  same way: real `student/` and `coach/` segments.

## Not yet implemented (intentionally, per MVP scope doc)
- Embedding generation (`embed_text` is a stub — wire up your provider)
- AI training-plan generation / recommendations (service seams exist)
- Advanced video analysis, gamification, payments, social features
