import os
from typing import Generator
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gbm_tracker.db")

engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Use this with FastAPI's Depends() for dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database() -> None:
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)

def drop_database() -> None:
    """
    Drop all database tables.
    WARNING: This will delete all data!
    """
    Base.metadata.drop_all(bind=engine)

def init_db() -> None:
    """
    Initialize the database with tables.
    This function can be called at application startup.
    """
    create_database()

def get_db_session() -> Session:
    """
    Get a database session for direct use outside of FastAPI.
    Remember to close the session when done.
    """
    return SessionLocal()

def check_database_connection() -> bool:
    """
    Check if database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1")).fetchone()
            return result is not None
    except Exception:
        return False

def get_database_info() -> dict:
    """
    Get information about the database.
    """
    return {
        "database_url": DATABASE_URL,
        "engine": str(engine.url),
        "connection_working": check_database_connection()
    }