import models
from database import db_manager
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date, timedelta
import random


def run():
    """Seed the database with initial data."""
    # Create session directly instead of using the generator
    db = db_manager.SessionLocal()
    try:
        # Check existing data
        existing_tags = db.query(models.Tag).count()
        existing_habits = db.query(models.Habit).count()
        existing_logs = db.query(models.HabitLog).count()

        print(f"Found {existing_tags} tags, {existing_habits} habits, and {existing_logs} logs in database.")

        # Get or create tags
        tag_names = ["Health", "Productivity", "Wellness", "Fitness", "Mindfulness", "Learning", "Social", "Finance"]
        tags = []

        for tag_name in tag_names:
            existing_tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
            if existing_tag:
                tags.append(existing_tag)
                print(f"Using existing tag: {tag_name}")
            else:
                new_tag = models.Tag(name=tag_name)
                db.add(new_tag)
                tags.append(new_tag)
                print(f"Creating new tag: {tag_name}")

        db.commit()

        # Refresh tags to ensure they have IDs
        for tag in tags:
            db.refresh(tag)

        # Define sample habits data
        today = date.today()
        start_date = today - timedelta(days=30)  # Start habits 30 days ago for better demo

        sample_habits_data = [
            {
                "title": "Drink 8 glasses of water",
                "description": "Stay hydrated by drinking at least 8 glasses of water daily",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": start_date,
                "reminder": True,
                "icon": "💧",
                "tag_names": ["Health"]
            },
            {
                "title": "Morning meditation",
                "description": "Practice mindfulness meditation for 10 minutes each morning",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": start_date,
                "reminder": True,
                "icon": "🧘",
                "tag_names": ["Mindfulness", "Wellness"]
            },
            {
                "title": "Exercise workout",
                "description": "Complete a 30-minute workout session",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": start_date,
                "reminder": True,
                "icon": "💪",
                "tag_names": ["Fitness", "Health"]
            },
            {
                "title": "Read for 30 minutes",
                "description": "Read books or educational material for personal growth",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": start_date,
                "reminder": False,
                "icon": "📚",
                "tag_names": ["Learning", "Productivity"]
            },
            {
                "title": "Weekly meal prep",
                "description": "Prepare healthy meals for the upcoming week",
                "periodicity": models.PeriodicityEnum.weekly,
                "frequency": 1,
                "select_days": "Sun",
                "start_date": start_date,
                "reminder": True,
                "icon": "🍽️",
                "tag_names": ["Health", "Productivity"]
            },
            {
                "title": "Call family/friends",
                "description": "Stay connected with loved ones through regular calls",
                "periodicity": models.PeriodicityEnum.weekly,
                "frequency": 2,
                "select_days": "Wed,Sun",
                "start_date": start_date,
                "reminder": True,
                "icon": "📞",
                "tag_names": ["Social"]
            },
            {
                "title": "Review monthly budget",
                "description": "Review and analyze monthly expenses and savings",
                "periodicity": models.PeriodicityEnum.monthly,
                "frequency": 1,
                "start_date": start_date,
                "reminder": True,
                "icon": "💰",
                "tag_names": ["Finance"]
            },
            {
                "title": "Learn something new",
                "description": "Spend time learning a new skill or taking an online course",
                "periodicity": models.PeriodicityEnum.weekly,
                "frequency": 3,
                "select_days": "Mon,Wed,Fri",
                "start_date": start_date,
                "reminder": False,
                "icon": "🎓",
                "tag_names": ["Learning", "Productivity"]
            }
        ]

        # Get or create habits
        habits = []
        created_habits = []

        for habit_data in sample_habits_data:
            # Extract tag_names for later use
            tag_names_for_habit = habit_data.pop("tag_names", [])

            # Check if habit already exists
            existing_habit = db.query(models.Habit).filter(models.Habit.title == habit_data["title"]).first()

            if existing_habit:
                habits.append(existing_habit)
                print(f"Using existing habit: {habit_data['title']}")
            else:
                new_habit = models.Habit(**habit_data)
                db.add(new_habit)
                habits.append(new_habit)
                created_habits.append((new_habit, tag_names_for_habit))
                print(f"Creating new habit: {habit_data['title']}")

        db.commit()

        # Refresh habits to ensure they have IDs
        for habit in habits:
            db.refresh(habit)

        # Assign tags to newly created habits only
        tags_dict = {tag.name: tag for tag in tags}

        for habit, tag_names_for_habit in created_habits:
            try:
                for tag_name in tag_names_for_habit:
                    if tag_name in tags_dict:
                        if tags_dict[tag_name] not in habit.tags:
                            habit.tags.append(tags_dict[tag_name])
                            print(f"Assigned tag '{tag_name}' to habit '{habit.title}'")
            except Exception as e:
                print(f"Error assigning tags to habit '{habit.title}': {e}")

        db.commit()

        # Create sample habit logs only for habits that don't have logs yet
        habit_logs = []

        for habit in habits:
            # Check if this habit already has logs
            existing_log_count = db.query(models.HabitLog).filter(models.HabitLog.habit_id == habit.id).count()

            if existing_log_count > 0:
                print(f"Habit '{habit.title}' already has {existing_log_count} logs, skipping log generation.")
                continue

            print(f"Generating sample logs for habit: {habit.title}")
            current_date = habit.start_date

            while current_date <= today:
                # Create realistic completion patterns
                should_complete = False

                if habit.periodicity == models.PeriodicityEnum.daily:
                    # Daily habits: 70-90% completion rate with some realistic gaps
                    completion_rate = 0.8 if habit.title in ["Drink 8 glasses of water", "Morning meditation"] else 0.7
                    should_complete = random.random() < completion_rate

                elif habit.periodicity == models.PeriodicityEnum.weekly:
                    # Weekly habits: Complete on specific days of the week
                    if habit.select_days:
                        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                        current_day = day_names[current_date.weekday()]
                        if current_day in habit.select_days:
                            should_complete = random.random() < 0.8  # 80% completion on target days
                    else:
                        # Complete once per week randomly
                        should_complete = current_date.weekday() == 6 and random.random() < 0.75  # Sunday, 75% chance

                elif habit.periodicity == models.PeriodicityEnum.monthly:
                    # Monthly habits: Complete once per month, usually at the end
                    if current_date.day >= 25:  # Last week of month
                        should_complete = random.random() < 0.9  # 90% completion rate for monthly habits

                if should_complete:
                    log = models.HabitLog(
                        habit_id=habit.id,
                        log_date=current_date,
                        completed=True,
                        notes=f"Completed {habit.title}",
                        completed_at=datetime.combine(current_date,
                                                      datetime.min.time().replace(hour=random.randint(6, 22)))
                    )
                    habit_logs.append(log)

                current_date += timedelta(days=1)

        # Add all new habit logs
        if habit_logs:
            db.add_all(habit_logs)
            db.commit()
            print(f"Created {len(habit_logs)} new habit log entries.")
        else:
            print("No new habit logs created (all habits already have logs).")

        # Final counts
        final_tag_count = db.query(models.Tag).count()
        final_habit_count = db.query(models.Habit).count()
        final_log_count = db.query(models.HabitLog).count()

        print(f"\nDatabase seeding completed!")
        print(f"Final counts - Tags: {final_tag_count}, Habits: {final_habit_count}, Logs: {final_log_count}")

        # Display some streak information for all habits
        print("\n--- Habit Streak Information ---")
        for habit in habits:
            try:
                current_streak = habit.get_current_streak(db)
                longest_streak = habit.get_longest_streak(db)
                is_completed = habit.is_completed_today(db)
                print(
                    f"{habit.title}: Current Streak: {current_streak}, Longest: {longest_streak}, Today: {'✅' if is_completed else '❌'}")
            except Exception as e:
                print(f"{habit.title}: Error calculating streaks - {e}")


    except IntegrityError as e:
        print(f"Integrity error (possibly duplicate data): {e}")
        db.rollback()
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


def seed_with_upsert():
    """Alternative seeding method that handles duplicates gracefully."""
    # Create session directly instead of using the generator
    db = db_manager.SessionLocal()
    try:

        # Define initial tags
        tag_names = ["Health", "Productivity", "Wellness", "Fitness", "Mindfulness", "Learning", "Social", "Finance"]

        # Add tags
        added_tags = 0
        for tag_name in tag_names:
            existing_tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
            if not existing_tag:
                new_tag = models.Tag(name=tag_name)
                db.add(new_tag)
                added_tags += 1

        db.commit()
        print(f"Added {added_tags} new tags to the database.")

        # Define sample habits with correct field structure
        today = date.today()
        sample_habits = [
            {
                "title": "Drink 8 glasses of water",
                "description": "Stay hydrated by drinking at least 8 glasses of water daily",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": today,
                "reminder": True,
                "icon": "💧"
            },
            {
                "title": "Morning meditation",
                "description": "Practice mindfulness meditation for 10 minutes each morning",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": today,
                "reminder": True,
                "icon": "🧘"
            },
            {
                "title": "Exercise workout",
                "description": "Complete a 30-minute workout session",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": today,
                "reminder": True,
                "icon": "💪"
            },
            {
                "title": "Read for 30 minutes",
                "description": "Read books or educational material for personal growth",
                "periodicity": models.PeriodicityEnum.daily,
                "frequency": 1,
                "start_date": today,
                "reminder": False,
                "icon": "📚"
            },
            {
                "title": "Weekly meal prep",
                "description": "Prepare healthy meals for the upcoming week",
                "periodicity": models.PeriodicityEnum.weekly,
                "frequency": 1,
                "select_days": "Sun",
                "start_date": today,
                "reminder": True,
                "icon": "🍽️"
            },
            {
                "title": "Call family/friends",
                "description": "Stay connected with loved ones through regular calls",
                "periodicity": models.PeriodicityEnum.weekly,
                "frequency": 2,
                "select_days": "Wed,Sun",
                "start_date": today,
                "reminder": True,
                "icon": "📞"
            }
        ]

        # Add habits
        added_habits = 0
        for habit_data in sample_habits:
            existing_habit = db.query(models.Habit).filter(models.Habit.title == habit_data["title"]).first()
            if not existing_habit:
                new_habit = models.Habit(**habit_data)
                db.add(new_habit)
                added_habits += 1

        db.commit()
        print(f"Added {added_habits} new habits to the database.")

        # Show all data
        all_tags = db.query(models.Tag).all()
        all_habits = db.query(models.Habit).all()
        print(f"All tags in database: {[tag.name for tag in all_tags]}")
        print(f"All habits in database: {[habit.title for habit in all_habits]}")

    except Exception as e:
        print(f"Error in upsert seeding: {e}")
        db.rollback()
    finally:
        db.close()


def initialize_and_seed():
    """Initialize database and then seed it."""
    try:
        # Initialize database first
        db_manager.initialize_database()
        print("Database initialized successfully.")

        # Then seed it
        run()

    except Exception as e:
        print(f"Error initializing database: {e}")


if __name__ == "__main__":
    print("Initializing and seeding database...")
    initialize_and_seed()