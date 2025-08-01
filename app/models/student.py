from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.parent import Parent
    from app.models.rate import Rate

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    forename: Mapped[str] = mapped_column(nullable=False, index=True)
    surname: Mapped[str] = mapped_column(nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    
    parent_id: Mapped[int] = mapped_column(ForeignKey("parents.id"), nullable=False)
    parent: Mapped[Parent] = relationship(back_populates="students")

    rates: Mapped[list[Rate]] = relationship(back_populates="student", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self) -> str:
        return (
            f"Student(id={self.id}, forename={self.forename!r}, "
            f"surname={self.surname!r}, is_active={self.is_active}, "
            f"created_at={self.created_at}, parent_id={self.parent_id})"
        )
    
    def __str__(self) -> str:
        status = "Active" if self.is_active is True else "Inactive"
        return f"ID {self.id} - {self.forename} {self.surname} - ({status}) - ParentID {self.parent_id}"




