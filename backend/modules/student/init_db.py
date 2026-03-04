from sqlalchemy import create_engine
from models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./student_analytics.db")

def init_database():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print(f"Database location: {DATABASE_URL}")

if __name__ == "__main__":
    init_database()