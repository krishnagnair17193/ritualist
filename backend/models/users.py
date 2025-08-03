from sqlalchemy import Column, String, Boolean, Date, Integer, Enum, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base, Session
from datetime import datetime, date, timedelta
import enum

from database import Base  # Assuming you have a database.py that defines Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="user", cascade="all, delete-orphan")