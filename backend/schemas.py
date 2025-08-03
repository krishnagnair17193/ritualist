from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class PeriodicityEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None


class HabitCreate(HabitBase):
    tag_ids: List[int] = []


class Habit(HabitBase):
    id: int
    tags: List['Tag'] = []

    # These fields will be populated by the API for the dashboard
    completed: Optional[bool] = False
    streak: Optional[int] = 0

    class Config:
        from_attributes = True


# If you want to implement proper habit logging, add these models:
class HabitLogBase(BaseModel):
    habit_id: int
    date: date
    completed: bool = False
    notes: Optional[str] = None


class HabitLogCreate(HabitLogBase):
    pass


class HabitLog(HabitLogBase):
    id: int

    class Config:
        from_attributes = True


# For the toggle response
class ToggleResponse(BaseModel):
    message: str
    habit_id: int
    date: str
    success: bool


# For habit statistics
class HabitStats(BaseModel):
    habit_id: int
    total_days: int
    completed_days: int
    completion_rate: float
    current_streak: int
    longest_streak: int

class ToggleHabitRequest(BaseModel):
    date: Optional[str] = None