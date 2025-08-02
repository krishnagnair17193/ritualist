import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def create_database_if_not_exists(self):
        """Create database if it doesn't exist"""
        try:
            # Connect to PostgreSQL server (not specific database)
            temp_engine = create_engine(settings.database_url_without_db)

            with temp_engine.connect() as conn:
                # Check if database exists
                result = conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                    {"db_name": settings.database_name}
                )

                if not result.fetchone():
                    # Create database
                    conn.execute(text("COMMIT"))  # End current transaction
                    conn.execute(text(f"CREATE DATABASE {settings.database_name}"))
                    logger.info(f"Database '{settings.database_name}' created successfully")
                else:
                    logger.info(f"Database '{settings.database_name}' already exists")

            temp_engine.dispose()

        except OperationalError as e:
            logger.error(f"Error creating database: {e}")
            raise

    def initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            # First, ensure database exists
            self.create_database_if_not_exists()

            # Create engine for the specific database
            self.engine = create_engine(settings.database_url)

            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database connection successful")

            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

            # Create all tables
            self.create_tables()

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def create_tables(self):
        """Create all tables defined in models"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("All tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise

    def get_db(self):
        """Dependency to get database session"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# Create global database manager instance
db_manager = DatabaseManager()
