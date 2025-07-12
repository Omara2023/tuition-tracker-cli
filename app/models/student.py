from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
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

    def __repr__(self) -> str:
        return (
            f"Student(id={self.id}, forename={self.forename!r}, "
            f"surname={self.surname!r}, is_active={self.is_active}, "
            f"created_at={self.created_at}, parent_id={self.parent_id})"
        )
    
    def __str__(self) -> str:
        status = "Active" if self.is_active is True else "Inactive"
        return f"ID {self.id} - {self.forename} {self.surname} - ({status}) - ParentID {self.parent_id}"




