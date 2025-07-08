from sqlalchemy import Column, Integer, ForeignKey, Enum, Float, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from db.base import Base
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

    __table_args__ = (
        UniqueConstraint("student_id", "level", name="uq_student_level"),
    )

    @property
    def student(self):
        return self.rate.student