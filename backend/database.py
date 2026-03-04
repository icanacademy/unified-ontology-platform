from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration for unified system
DATABASE_DIR = os.path.join(os.path.dirname(__file__), "databases")

# Ensure databases directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

# Individual platform databases preserved
DATABASES = {
    "books": f"sqlite:///{DATABASE_DIR}/books_library.db",
    "faculty": f"sqlite:///{DATABASE_DIR}/faculty_analytics.db", 
    "students": f"sqlite:///{DATABASE_DIR}/student_analytics.db",
    "classes": f"sqlite:///{DATABASE_DIR}/ican_classes.db",
    "ontology": f"sqlite:///{DATABASE_DIR}/ontology_platform.db"
}

# Create engines for each database
engines = {}
SessionLocals = {}
Bases = {}

for platform, database_url in DATABASES.items():
    engines[platform] = create_engine(database_url, connect_args={"check_same_thread": False})
    SessionLocals[platform] = sessionmaker(autocommit=False, autoflush=False, bind=engines[platform])
    Bases[platform] = declarative_base()

# Default database configuration (books for main system)
SQLALCHEMY_DATABASE_URL = DATABASES["books"]
engine = engines["books"]
SessionLocal = SessionLocals["books"]
Base = Bases["books"]

def get_db(platform: str = "books"):
    """Get database session for specified platform"""
    if platform not in SessionLocals:
        platform = "books"
    
    db = SessionLocals[platform]()
    try:
        yield db
    finally:
        db.close()

def get_engine(platform: str = "books"):
    """Get database engine for specified platform"""
    return engines.get(platform, engines["books"])

def get_session_local(platform: str = "books"):
    """Get SessionLocal for specified platform"""
    return SessionLocals.get(platform, SessionLocals["books"])