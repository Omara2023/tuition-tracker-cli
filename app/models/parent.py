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

