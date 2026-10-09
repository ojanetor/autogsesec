"""Database models for runtime data: exercise sessions and responses.

Scenario content and rubrics are NOT stored here; they live in data/ as
versioned JSON. No column identifies a person.
"""
import uuid
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utc_now():
    return datetime.now(timezone.utc)


def new_session_id():
    return str(uuid.uuid4())


class ExerciseSession(db.Model):
    __tablename__ = "sessions"

    session_id = db.Column(db.String(36), primary_key=True, default=new_session_id)
    scenario_id = db.Column(db.String(20), nullable=False)
    content_version = db.Column(db.String(120), nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    completed_at = db.Column(db.DateTime(timezone=True))
    pre_understanding = db.Column(db.Integer)
    post_understanding = db.Column(db.Integer)

    responses = db.relationship(
        "Response", back_populates="session",
        cascade="all, delete-orphan", order_by="Response.response_id",
    )


class Response(db.Model):
    __tablename__ = "responses"
    __table_args__ = (
        db.UniqueConstraint("session_id", "decision_point_id", name="one_answer_per_decision"),
    )

    response_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.String(36), db.ForeignKey("sessions.session_id"), nullable=False, index=True
    )
    decision_point_id = db.Column(db.String(20), nullable=False)
    option_id = db.Column(db.String(5), nullable=False)
    submitted_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    session = db.relationship("ExerciseSession", back_populates="responses")