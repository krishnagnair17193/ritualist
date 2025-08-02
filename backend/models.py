from sqlalchemy import Column, Integer, String, Text, Enum, Date, Boolean, Table, ForeignKey, ARRAY
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class PeriodicityEnum(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

habit_tags = Table(
    "habit_tags",
    Base.metadata,
    Column("habit_id", Integer, ForeignKey("habits.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"))
)

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # You can link to a users table
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    periodicity = Column(Enum(PeriodicityEnum), nullable=False)
    frequency = Column(Integer, default=1)
    selected_days = Column(ARRAY(String), nullable=True)  # For weekly habits
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    icon = Column(String(10), nullable=True)
    is_reminder = Column(Boolean, default=False)

    tags = relationship("Tag", secondary=habit_tags, back_populates="habits")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    habits = relationship("Habit", secondary=habit_tags, back_populates="tags")