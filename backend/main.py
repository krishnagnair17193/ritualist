from fastapi import FastAPI, HTTPException, Depends
import logging

logger = logging.getLogger("uvicorn.error")
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session, declarative_base
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import schemas
import models
from database import db_manager
app = FastAPI()

# Allow frontend to connect (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only. Restrict this in prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(db_manager.get_db)):
    db_tag = models.Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@app.get("/tags/", response_model=List[schemas.Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(db_manager.get_db)):
    return db.query(models.Tag).offset(skip).limit(limit).all()

@app.post("/habits/", response_model=schemas.Habit)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(db_manager.get_db)):
    db_tags = db.query(models.Tag).filter(models.Tag.id.in_(habit.tag_ids)).all()
    db_habit = models.Habit(**habit.dict(exclude={"tag_ids"}))
    db_habit.tags = db_tags
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@app.get("/habits/", response_model=List[schemas.Habit])
def read_habits(skip: int = 0, limit: int = 100, db: Session = Depends(db_manager.get_db)):
    return db.query(models.Habit).offset(skip).limit(limit).all()

@app.get("/habits/{habit_id}", response_model=schemas.Habit)
def read_habit(habit_id: int, db: Session = Depends(db_manager.get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@app.delete("/habits/{habit_id}", response_model=schemas.Habit)
def delete_habit(habit_id: int, db: Session = Depends(db_manager.get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return habit

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        db_manager.initialize_database()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise