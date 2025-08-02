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
    periodicity: PeriodicityEnum
    frequency: Optional[int] = None
    select_days: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    reminder: bool = False
    icon: Optional[str] = None
    tag_ids: List[int] = []

class HabitCreate(HabitBase):
    pass

class Habit(HabitBase):
    id: int
    tags: List[Tag]

    class Config:
        orm_mode = True