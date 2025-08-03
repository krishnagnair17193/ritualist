from fastapi import FastAPI, HTTPException, Depends
import logging

logger = logging.getLogger("uvicorn.error")
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, scoped_session, declarative_base
from typing import List, Optional
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


@app.get("/habits/logs/", response_model=List[schemas.Habit])
def get_habit_logs(
        date: Optional[str] = None,
        db: Session = Depends(db_manager.get_db)
):
    """
    Get habit logs for a specific date.
    If no date provided, returns habits for today.
    """
    try:
        # Parse the date if provided, otherwise use today
        if date:
            # Validate date format (YYYY-MM-DD)
            from datetime import datetime
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            from datetime import date as datetime_date
            parsed_date = datetime_date.today()

        # For now, return all habits (you can modify this to filter by date when you add habit logs)
        habits = db.query(models.Habit).all()
        print(f"habits: {habits}")
        # Add a mock 'completed' field for demo purposes
        # You'll want to replace this with actual habit log data
        for habit in habits:
            # Mock completion status (you can replace this with real logic)
            habit.completed = habit.has_completed_on_date(db, parsed_date)
            habit.streak = habit.get_current_streak(db)

        return habits

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error fetching habit logs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/habits/{habit_id}/toggle")
def toggle_habit(
        habit_id: int,
        request_body: schemas.ToggleHabitRequest,
        db: Session = Depends(db_manager.get_db)
):
    """
    Toggle completion status of a habit for a specific date.
    """
    try:
        # Check if habit exists
        habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
        if habit is None:
            raise HTTPException(status_code=404, detail="Habit not found")

        # Parse the date if provided, otherwise use today
        if request_body.date:
            try:
                from datetime import datetime
                parsed_date = datetime.strptime(request_body.date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        else:
            from datetime import date as datetime_date
            parsed_date = datetime_date.today()

        # Here you would typically:
        # 1. Check if a habit log exists for this habit and date
        # 2. If it exists, toggle its completion status
        # 3. If it doesn't exist, create a new habit log entry
        habit_log = db.query(models.HabitLog).filter(
            models.HabitLog.habit_id == habit_id,
            models.HabitLog.log_date == parsed_date
        ).first()
        if habit_log:
            # Toggle completion status
            habit_log.completed = not habit_log.completed
            db.commit()
        else:
            # Create a new habit log entry with default completion status
            new_log = models.HabitLog(habit_id=habit_id, log_date=parsed_date, completed=True)
            db.add(new_log)
            db.commit()

        # For now, we'll just return a success response
        # You'll need to implement actual habit log functionality

        return {
            "message": f"Habit {habit_id} toggled for {parsed_date}",
            "habit_id": habit_id,
            "date": str(parsed_date),
            "success": True
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        logger.error(f"Error toggling habit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Optional: Add an endpoint to get habit statistics
@app.get("/habits/{habit_id}/stats")
def get_habit_stats(
        habit_id: int,
        db: Session = Depends(db_manager.get_db)
):
    """
    Get statistics for a specific habit (completion rate, streak, etc.)
    """
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Mock stats for now - replace with real calculations
    return {
        "habit_id": habit_id,
        "total_days": 30,
        "completed_days": 20,
        "completion_rate": 66.7,
        "current_streak": 5,
        "longest_streak": 12
    }

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        db_manager.initialize_database()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


# Add these imports to your FastAPI app
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import jwt
import hashlib
import secrets

# Configuration - add these to your environment variables
SECRET_KEY = "your-secret-key-here-change-in-production"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


# Pydantic models for authentication
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    user: dict


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: Optional[str] = None


# Utility functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str) -> str:
    """Simple password hashing - use bcrypt in production"""
    salt = "your-salt-here"  # Use a proper salt in production
    return hashlib.sha256((password + salt).encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password


# Authentication endpoints
@app.post("/auth/register", response_model=Token)
def register_user(user_data: UserRegister, db: Session = Depends(db_manager.get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = hash_password(user_data.password)
        db_user = models.User(
            email=user_data.email,
            name=user_data.name or user_data.email.split("@")[0],
            password_hash=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email, "user_id": db_user.id},
            expires_delta=access_token_expires
        )

        # Create refresh token
        refresh_token = create_access_token(
            data={"sub": db_user.email, "type": "refresh"},
            expires_delta=timedelta(days=7)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
            "user": {
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@app.post("/auth/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(db_manager.get_db)):
    """Authenticate user and return token"""
    try:
        # Find user by email
        user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(user_credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )

        # Create refresh token
        refresh_token = create_access_token(
            data={"sub": user.email, "type": "refresh"},
            expires_delta=timedelta(days=7)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@app.get("/auth/me", response_model=UserResponse)
def get_current_user(current_user_email: str = Depends(verify_token), db: Session = Depends(db_manager.get_db)):
    """Get current user information"""
    user = db.query(models.User).filter(models.User.email == current_user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": str(user.created_at) if hasattr(user, 'created_at') else None
    }


@app.post("/auth/logout")
def logout_user(current_user_email: str = Depends(verify_token)):
    """Logout user (invalidate token)"""
    # In a production app, you'd want to blacklist the token
    # For now, we'll just return success
    return {"message": "Successfully logged out"}


# Protected route example
@app.get("/protected")
def protected_route(current_user_email: str = Depends(verify_token)):
    """Example of a protected route that requires authentication"""
    return {"message": f"Hello {current_user_email}, this is a protected route!"}