from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime, timezone

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    forename = Column(String(50), index=True, nullable=False)
    surname = Column(String(50), index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False) 
   
    parent = relationship("Parent", back_populates="students")
    rates = relationship("Rate", back_populates="student", cascade="all, delete-orphan")

