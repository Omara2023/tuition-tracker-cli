from __future__ import annotations
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.lesson import Lesson
    from app.models.payment import Payment

class LessonPayment(Base):
    __tablename__ = "lesson_payments"

    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"), primary_key=True)
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="lesson_payments")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="lesson_payments")
