from sqlalchemy import Column, Integer, ForeignKey, Enum, Float, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class Subjects(enum.Enum):
    MATHEMATICS = "Mathematics"
    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"

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


    @property
    def student(self):
        return self.rate.student