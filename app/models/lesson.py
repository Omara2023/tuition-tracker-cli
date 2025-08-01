from __future__ import annotations
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as SAEnum
from app.db.base import Base
from typing import TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from app.models.rate import Rate
    from app.models.payment import Payment
    from app.models.lesson_payment import LessonPayment

class Subjects(enum.Enum):
    MATHEMATICS = "Mathematics"
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"

    def __str__(self) -> str:
        return f"{self.value}"

class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    rate_id: Mapped[int] = mapped_column(ForeignKey("rates.id"), nullable=False)
    subject: Mapped[Subjects] = mapped_column(SAEnum(Subjects), nullable=False)
    duration: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(nullable=False)
    
    rate: Mapped[Rate] = relationship(back_populates="lessons")
    lesson_payments: Mapped[list[LessonPayment]] = relationship(back_populates="lesson", cascade="all, delete-orphan", lazy="selectin")
    
    payments: Mapped[list[Payment]] = relationship(secondary="lesson_payments", back_populates="lessons", viewonly=True, lazy="selectin")

    def __repr__(self) -> str:
        return (
            f"Lesson(id={self.id}, rate_id={self.rate_id},"
            f"subject={self.subject}, duration={self.duration}, date={self.date})"
        )
    
    def __str__(self) -> str:
        rate = getattr(self, "rate", None)
        return (
            f"{self.id} - {rate} - {self.subject} - "
            f"{self.duration}hrs - {self.date}"
        )
    
    @property
    def student(self):
        return self.rate.student
    
def string_to_subject_enum(input_string: str) -> Subjects:
    "Converter function to transform text input to enum."
    match input_string.strip().lower():
        case "mathematics":
            return Subjects.MATHEMATICS
        case "biology":
            return Subjects.BIOLOGY
        case "chemistry":
            return Subjects.CHEMISTRY
        case "physics":
            return Subjects.PHYSICS
        case _:
            raise ValueError(f"Invalid subject: {input_string!r}")