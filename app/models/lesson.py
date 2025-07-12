from sqlalchemy import Column, Integer, ForeignKey, Enum, Float, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class Subjects(enum.Enum):
    MATHEMATICS = "Mathematics"
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"

    def __str__(self) -> str:
        return f"{self.value}"

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    rate_id = Column(Integer, ForeignKey("rates.id"), nullable=False)
    subject = Column(Enum(Subjects), nullable=False)
    duration = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    
    rate = relationship("Rate", back_populates="lessons")
    lesson_payments = relationship("LessonPayment", back_populates="lesson", cascade="all, delete-orphan")
    
    payments = relationship(
        "Payment",
        secondary="lesson_payments",
        viewonly=True,
        back_populates="lessons",
    )

    def __repr__(self) -> str:
        return (
            f"Lesson(id={self.id},rate_id={self.rate_id},"
            f"subject={self.subject},duration={self.duration}"
            f"date={self.date})"
        )
    
    def __str__(self) -> str:
        return f"{self.id} - {self.rate} - {self.subject} - {self.duration}hrs - {self.date}"


    @property
    def student(self):
        return self.rate.student