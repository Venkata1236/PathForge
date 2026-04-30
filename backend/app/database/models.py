from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(String, primary_key=True)
    learner_name = Column(String(100), nullable=False)
    target_role = Column(String(100), nullable=False)
    experience_level = Column(String(20), nullable=False)
    hours_per_week = Column(Integer, nullable=False)
    total_weeks = Column(Integer, nullable=False)
    skill_gaps_count = Column(Integer, nullable=False)
    courses_count = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)
    processing_time = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
