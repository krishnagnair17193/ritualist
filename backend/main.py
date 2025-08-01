from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only. Restrict this in prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory fake DB for now
habits_db = []

class Habit(BaseModel):
    id: int
    name: str
    description: str = ""
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "FastAPI is running 🚀"}

@app.get("/habits", response_model=List[Habit])
def get_habits():
    return habits_db

@app.post("/habits", response_model=Habit)
def create_habit(habit: Habit):
    habits_db.append(habit)
    return habit

@app.get("/habits/{habit_id}", response_model=Habit)
def get_habit(habit_id: int):
    for habit in habits_db:
        if habit.id == habit_id:
            return habit
    raise HTTPException(status_code=404, detail="Habit not found")

@app.put("/habits/{habit_id}", response_model=Habit)
def update_habit(habit_id: int, updated_habit: Habit):
    for i, habit in enumerate(habits_db):
        if habit.id == habit_id:
            habits_db[i] = updated_habit
            return updated_habit
    raise HTTPException(status_code=404, detail="Habit not found")

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int):
    global habits_db
    habits_db = [habit for habit in habits_db if habit.id != habit_id]
    return {"message": "Habit deleted"}