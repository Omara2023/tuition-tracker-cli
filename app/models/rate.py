from sqlalchemy import Column, Integer, ForeignKey, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class RateLevel(enum.Enum):
    GCSE = "GCSE"
    A_LEVEL = "A-Level"


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    level = Column(Enum(RateLevel), nullable=False)
    hourly_rate = Column(Float, nullable=False)

    student = relationship("Student", back_populates="rates")
    lessons = relationship("Lesson", back_populates="rate", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint("student_id", "level", name="uq_student_level"),
    )

def string_to_level_enum(input: str) -> RateLevel:
    """Helper method to translate user input to enum."""
    mapping = {
        "gcse": RateLevel.GCSE,
        "a-level": RateLevel.A_LEVEL,
    }
    try:
        return mapping[input.strip().lower()]
    except KeyError:
        raise ValueError(f"Invalid rate level: {input!r}")
