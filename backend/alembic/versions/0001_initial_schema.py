"""initial schema: users, coach_students, sports, skills, drills,
training_plans, training_assignments, student_skill_progress,
practice_evidence, coach_custom_data, drill_embeddings, skill_embeddings

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

EMBEDDING_DIM = 1536


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "sports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String, nullable=False, unique=True, index=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("image_url", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "coach_students",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("coach_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "skills",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("sport_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sports.id"), index=True),
        sa.Column("parent_skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), nullable=True, index=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("skill_level", sa.String, nullable=True),
        sa.Column("prerequisites", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "drills",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("sport_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sports.id"), index=True),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), nullable=True, index=True),
        sa.Column("drill_name", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("skill_level", sa.String, nullable=True),
        sa.Column("sets", sa.Integer, nullable=True),
        sa.Column("reps", sa.Integer, nullable=True),
        sa.Column("duration_minutes", sa.Integer, nullable=True),
        sa.Column("video_url", sa.String, nullable=True),
        sa.Column("is_custom", sa.Boolean, nullable=False, server_default=sa.false(), index=True),
        sa.Column("created_by_coach_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "training_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True),
        sa.Column("sport_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sports.id"), index=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("source_type", sa.String, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("start_date", sa.Date, nullable=True),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "training_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("training_plan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("training_plans.id"), index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True),
        sa.Column("day_number", sa.Integer, nullable=True),
        sa.Column("scheduled_date", sa.Date, nullable=True, index=True),
        sa.Column("drill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("drills.id")),
        sa.Column("sets", sa.Integer, nullable=True),
        sa.Column("reps", sa.Integer, nullable=True),
        sa.Column("status", sa.String, nullable=False, index=True),
        sa.Column("notes", sa.String, nullable=True),
    )

    op.create_table(
        "student_skill_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), index=True),
        sa.Column("mastery_score", sa.Float, nullable=False, server_default="0"),
        sa.Column("proficiency_level", sa.String, nullable=True),
        sa.Column("last_practiced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "practice_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True),
        sa.Column("training_assignment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("training_assignments.id"), index=True),
        sa.Column("video_url", sa.String, nullable=True),
        sa.Column("cloudinary_public_id", sa.String, nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("coach_feedback", sa.String, nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "coach_custom_data",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("coach_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True, index=True),
        sa.Column("data_type", sa.String, nullable=False),
        sa.Column("payload", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "drill_embeddings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("drill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("drills.id"), unique=True, index=True),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
        sa.Column("source_text", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "skill_embeddings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("skill_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("skills.id"), unique=True, index=True),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
        sa.Column("source_text", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("skill_embeddings")
    op.drop_table("drill_embeddings")
    op.drop_table("coach_custom_data")
    op.drop_table("practice_evidence")
    op.drop_table("student_skill_progress")
    op.drop_table("training_assignments")
    op.drop_table("training_plans")
    op.drop_table("drills")
    op.drop_table("skills")
    op.drop_table("coach_students")
    op.drop_table("sports")
    op.drop_table("users")
