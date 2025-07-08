from sqlalchemy import Column, Integer, String, Boolean, DateTime
from db.base import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    forename = Column(String, nullable=False, index=True)
    surname = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    