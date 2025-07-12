from sqlalchemy import Column, Integer, ForeignKey, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class RateLevel(enum.Enum):
    GCSE = "GCSE"
    A_LEVEL = "A-Level"

    def __str__(self) -> str:
        return f"{self.value}"

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

    def __repr__(self) -> str:
        return (
            f"Rate(id={self.id}, student_id={self.student_id}, "
            f"level={self.level}, hourly_rate=£{self.hourly_rate:.2f} "
        )
    
    def __str__(self) -> str:
        return f"{self.id} - {self.student.forename} {self.student.surname} - {self.level} - £{self.hourly_rate:.2f}"

def string_to_level_enum(input_string: str) -> RateLevel:
    """Helper method to translate user input to enum."""
    mapping = {
        "gcse": RateLevel.GCSE,
        "a-level": RateLevel.A_LEVEL,
    }
    try:
        return mapping[input_string.strip().lower()]
    except KeyError:
        raise ValueError(f"Invalid rate level: {input_string!r}")
