from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base

class LessonPayment(Base):
    __tablename__ = "lesson_payments"

    lesson_id = Column(Integer, ForeignKey("lessons.id"), primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), primary_key=True)
    amount_paid = Column(Numeric(10, 2), nullable=False)

    lesson = relationship("Lesson", back_populates="lesson_payments")
    payment = relationship("Payment", back_populates="lesson_payments")
