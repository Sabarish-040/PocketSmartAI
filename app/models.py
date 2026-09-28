from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(120), nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    recommendations = relationship(
        "Recommendation",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    planner_type = Column(String(30), nullable=False)
    request_json = Column(Text, nullable=False)
    response_json = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="recommendations",
    )