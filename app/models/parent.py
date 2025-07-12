from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime, timezone

class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    forename = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    students = relationship("Student", back_populates="parent")
    payments = relationship("Payment", back_populates="parent")

    def __repr__(self) -> str:
        return (
            f"Parent(id={self.id}, forename={self.forename!r}, "
            f"surname={self.surname!r}, is_active={self.is_active}, "
            f"created_at={self.created_at})"
        )
    
    def __str__(self) -> str:
        status = "Active" if self.is_active is True else "Inactive"
        return f"{self.id} - {self.forename} {self.surname} - ({status})"


