from __future__ import annotations
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.parent import Parent
    from app.models.lesson import Lesson
    from app.models.lesson_payment import LessonPayment

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False, default= lambda: datetime.now(timezone.utc))
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False) 

    parent: Mapped[Parent] = relationship(back_populates="payments", lazy="selectin")
    lesson_payments: Mapped[list[LessonPayment]] = relationship(back_populates="payment", cascade="all, delete-orphan", lazy="selectin")
    lessons: Mapped[list[Lesson]] = relationship(secondary="lesson_payments", viewonly=True, back_populates="payments", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("timestamp", "parent_id", name="uix_parent_timestamp"),
    )
