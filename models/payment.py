from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now(timezone.utc), unique=True)
    amount = Column(Numeric(10, 2), nullable=False) 

    parent = relationship("Parent", back_populates="payments")
    lesson_payments = relationship("LessonPayment", back_populates="payment", cascade="all, delete-orphan")

    lessons = relationship(
        "Lesson",
        secondary="lesson_payments",
        viewonly=True,
        back_populates="payments",
    )

    __table_args__ = (
        UniqueConstraint("timestamp", "parent_id", name="uix_parent_timestamp"),
    )
