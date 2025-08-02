import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/your_database")
    database_host: str = os.getenv("DATABASE_HOST", "localhost")
    database_port: int = int(os.getenv("DATABASE_PORT", "5432"))
    database_name: str = os.getenv("DATABASE_NAME", "your_database")
    database_user: str = os.getenv("DATABASE_USER", "username")
    database_password: str = os.getenv("DATABASE_PASSWORD", "password")

    @property
    def database_url_without_db(self) -> str:
        """URL for connecting to PostgreSQL server without specifying database"""
        print(f"Connecting to PostgreSQL server at {self.database_host}:{self.database_port} as {self.database_user}")
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/postgres"


settings = Settings()
