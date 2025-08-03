from sqlalchemy import Column, String, Boolean, Date, Integer, Enum, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base, Session
from datetime import datetime, date, timedelta
import enum

from database import Base  # Assuming you have a database.py that defines Base


class PeriodicityEnum(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


# Association table for many-to-many relationship with tags
habit_tags = Table(
    'habit_tags',
    Base.metadata,
    Column('habit_id', Integer, ForeignKey('habits.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    periodicity = Column(Enum(PeriodicityEnum), nullable=False)
    frequency = Column(Integer, nullable=True)  # e.g., 3 times a week
    select_days = Column(String, nullable=True)  # Comma-separated days: "Mon,Wed,Fri"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    reminder = Column(Boolean, default=False)
    icon = Column(String, nullable=True)

    tags = relationship("Tag", secondary=habit_tags, back_populates="habits")
    habit_logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

    def has_completed_on_date(self, db: Session, log_date: date) -> bool:
        """Check if the habit was completed on a specific date."""
        log = db.query(HabitLog).filter(
            HabitLog.habit_id == self.id,
            HabitLog.log_date == log_date
        ).first()
        return log.completed if log else False

    def get_current_streak(self, db: Session) -> int:
        """Calculate the current streak for this habit."""
        today = date.today()

        if self.periodicity == PeriodicityEnum.daily:
            return self._calculate_daily_streak(db, today)
        elif self.periodicity == PeriodicityEnum.weekly:
            return self._calculate_weekly_streak(db, today)
        elif self.periodicity == PeriodicityEnum.monthly:
            return self._calculate_monthly_streak(db, today)

        return 0

    def _calculate_daily_streak(self, db: Session, today: date) -> int:
        """Calculate streak for daily habits."""
        streak = 0
        current_date = today

        while current_date >= self.start_date:
            log = db.query(HabitLog).filter(
                HabitLog.habit_id == self.id,
                HabitLog.log_date == current_date
            ).first()

            if log and log.completed:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break

        return streak

    def _calculate_weekly_streak(self, db: Session, today: date) -> int:
        """Calculate streak for weekly habits."""
        streak = 0
        current_week_start = today - timedelta(days=today.weekday())  # Monday of current week

        while current_week_start >= self.start_date:
            week_end = current_week_start + timedelta(days=6)  # Sunday of the week

            # Count completed logs in this week
            completed_logs = db.query(HabitLog).filter(
                HabitLog.habit_id == self.id,
                HabitLog.log_date >= current_week_start,
                HabitLog.log_date <= week_end,
                HabitLog.completed == True
            ).count()

            # Check if the weekly target was met
            target_frequency = self.frequency or 1
            if completed_logs >= target_frequency:
                streak += 1
                current_week_start -= timedelta(days=7)  # Previous week
            else:
                break

        return streak

    def _calculate_monthly_streak(self, db: Session, today: date) -> int:
        """Calculate streak for monthly habits."""
        streak = 0
        current_month_start = today.replace(day=1)

        while current_month_start >= self.start_date:
            # Get the last day of the current month
            if current_month_start.month == 12:
                next_month = current_month_start.replace(year=current_month_start.year + 1, month=1)
            else:
                next_month = current_month_start.replace(month=current_month_start.month + 1)

            month_end = next_month - timedelta(days=1)

            # Count completed logs in this month
            completed_logs = db.query(HabitLog).filter(
                HabitLog.habit_id == self.id,
                HabitLog.log_date >= current_month_start,
                HabitLog.log_date <= month_end,
                HabitLog.completed == True
            ).count()

            # Check if the monthly target was met
            target_frequency = self.frequency or 1
            if completed_logs >= target_frequency:
                streak += 1
                # Move to previous month
                if current_month_start.month == 1:
                    current_month_start = current_month_start.replace(year=current_month_start.year - 1, month=12)
                else:
                    current_month_start = current_month_start.replace(month=current_month_start.month - 1)
            else:
                break

        return streak

    def get_longest_streak(self, db: Session) -> int:
        """Calculate the longest streak ever achieved for this habit."""
        if self.periodicity == PeriodicityEnum.daily:
            return self._get_longest_daily_streak(db)
        elif self.periodicity == PeriodicityEnum.weekly:
            return self._get_longest_weekly_streak(db)
        elif self.periodicity == PeriodicityEnum.monthly:
            return self._get_longest_monthly_streak(db)

        return 0

    def _get_longest_daily_streak(self, db: Session) -> int:
        """Get longest streak for daily habits."""
        logs = db.query(HabitLog).filter(
            HabitLog.habit_id == self.id,
            HabitLog.completed == True
        ).order_by(HabitLog.log_date).all()

        if not logs:
            return 0

        longest_streak = 1
        current_streak = 1

        for i in range(1, len(logs)):
            expected_date = logs[i - 1].log_date + timedelta(days=1)
            if logs[i].log_date == expected_date:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1

        return longest_streak

    def _get_longest_weekly_streak(self, db: Session) -> int:
        """Get longest streak for weekly habits (simplified version)."""
        # This is a simplified version - could be enhanced with more complex logic
        weeks_with_completion = db.query(HabitLog).filter(
            HabitLog.habit_id == self.id,
            HabitLog.completed == True
        ).distinct().count()

        return min(weeks_with_completion, self.get_current_streak(db))

    def _get_longest_monthly_streak(self, db: Session) -> int:
        """Get longest streak for monthly habits (simplified version)."""
        # This is a simplified version - could be enhanced with more complex logic
        months_with_completion = db.query(HabitLog).filter(
            HabitLog.habit_id == self.id,
            HabitLog.completed == True
        ).distinct().count()

        return min(months_with_completion, self.get_current_streak(db))

    def is_completed_today(self, db: Session) -> bool:
        """Check if the habit was completed today."""
        today = date.today()
        log = db.query(HabitLog).filter(
            HabitLog.habit_id == self.id,
            HabitLog.log_date == today
        ).first()

        return log.completed if log else False

    def mark_completed(self, db: Session, log_date: date = None, notes: str = None) -> 'HabitLog':
        """Mark the habit as completed for a specific date."""
        if log_date is None:
            log_date = date.today()

        # Check if log already exists
        existing_log = db.query(HabitLog).filter(
            HabitLog.habit_id == self.id,
            HabitLog.log_date == log_date
        ).first()

        if existing_log:
            existing_log.completed = True
            existing_log.notes = notes
            existing_log.completed_at = datetime.now()
            log = existing_log
        else:
            log = HabitLog(
                habit_id=self.id,
                log_date=log_date,
                completed=True,
                notes=notes,
                completed_at=datetime.now()
            )
            db.add(log)

        db.commit()
        return log

    def mark_incomplete(self, db: Session, log_date: date = None) -> 'HabitLog':
        """Mark the habit as incomplete for a specific date."""
        if log_date is None:
            log_date = date.today()

        # Check if log already exists
        existing_log = db.query(HabitLog).filter(
            HabitLog.habit_id == self.id,
            HabitLog.log_date == log_date
        ).first()

        if existing_log:
            existing_log.completed = False
            existing_log.completed_at = None
            log = existing_log
        else:
            log = HabitLog(
                habit_id=self.id,
                log_date=log_date,
                completed=False
            )
            db.add(log)

        db.commit()
        return log


class HabitLog(Base):
    __tablename__ = 'habit_logs'

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey('habits.id'), nullable=False)
    log_date = Column(Date, nullable=False, index=True)
    completed = Column(Boolean, default=False, nullable=False)
    notes = Column(String, nullable=True)  # Optional notes for the log entry
    completed_at = Column(DateTime, nullable=True)  # Timestamp when marked as completed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    habit = relationship("Habit", back_populates="habit_logs")

    def __repr__(self):
        return f"<HabitLog(habit_id={self.habit_id}, date={self.log_date}, completed={self.completed})>"


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    habits = relationship("Habit", secondary=habit_tags, back_populates="tags")