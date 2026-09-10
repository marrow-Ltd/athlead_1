# Database schema (v1)

See `backend/alembic/versions/0001_initial_schema.py` for the executable
source of truth. Summary of tables:

| Table | Purpose |
|---|---|
| users | student / coach / admin accounts |
| coach_students | coach<->student relationship + status |
| sports | system sport catalog |
| skills | hierarchical skill tree per sport (self-referencing parent_skill_id) |
| drills | system + coach-custom drills |
| training_plans | a student's structured program for a sport |
| training_assignments | per-day drill assignment within a plan |
| student_skill_progress | mastery score per student/skill |
| practice_evidence | submitted video + coach feedback |
| coach_custom_data | free-form bucket for coach data that doesn't map 1:1 elsewhere |
| drill_embeddings / skill_embeddings | pgvector columns for semantic search/RAG |
