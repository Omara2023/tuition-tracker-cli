from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.payment import Payment

class Parent(Base):
    __tablename__ = "parents"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    forename: Mapped[str] = mapped_column(nullable=False, index=True)
    surname: Mapped[str] = mapped_column(nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column( default=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    students: Mapped[list["Student"]] = relationship("Student", back_populates="parent", cascade="all, delete-orphan", lazy="selectin")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="parent", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self) -> str:
        return (
            f"Parent(id={self.id}, forename={self.forename!r}, "
            f"surname={self.surname!r}, is_active={self.is_active}, "
             f"created_at={self.created_at.isoformat() if self.created_at else None})"
        )
    
    def __str__(self) -> str:
        status = "Active" if self.is_active is True else "Inactive"
        return f"{self.id} - {self.forename} {self.surname} - ({status})"


