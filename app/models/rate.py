from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, ForeignKey, Enum as SAEnum, UniqueConstraint
from decimal import Decimal
from app.db.base import Base
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.lesson import Lesson

class RateLevel(enum.Enum):
    GCSE = "GCSE"
    A_LEVEL = "A-Level"

    def __str__(self) -> str:
        return f"{self.value}"

class Rate(Base):
    __tablename__ = "rates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    level: Mapped[RateLevel] = mapped_column(SAEnum(RateLevel), nullable=False)
    hourly_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    student: Mapped["Student"] = relationship("Student", back_populates="rates")
    lessons: Mapped[list["Lesson"]] = relationship("Lesson", back_populates="rate", cascade="all, delete-orphan", lazy="selectin")
    
    __table_args__ = (
        UniqueConstraint("student_id", "level", name="uq_student_level"),
    )

    def __repr__(self) -> str:
        return (
            f"Rate(id={self.id}, student_id={self.student_id}, "
            f"level={self.level}, hourly_rate=£{self.hourly_rate:.2f} "
        )
    
    def __str__(self) -> str:
        student = getattr(self, "student", None)
        if student:
            return f"{self.id} - {student.forename} {student.surname} - {self.level} - £{self.hourly_rate:.2f}"
        return f"{self.id} - {self.level} - £{self.hourly_rate:.2f}"
    
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
