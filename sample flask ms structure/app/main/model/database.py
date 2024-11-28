from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database Configuration
# Use environment variables or a more robust configuration method
DATABASE_CONFIG = {
    'host': 'localhost',  # Make sure this is correct
    'user': 'root',       # Your MySQL username
    'password': 'Eventura@12',       # Your MySQL password (leave blank if no password)
    'database': 'apidata'  # Your database name
}

# Construct the database URI
DATABASE_URI = (
    f"mysql+pymysql://{DATABASE_CONFIG['user']}:"
    f"{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}/"
    f"{DATABASE_CONFIG['database']}"
)

# Create engine with additional configurations
engine = create_engine(
    DATABASE_URI, 
    echo=True,  # Set to False in production
    pool_pre_ping=True,  # Test connection before using
    pool_recycle=3600    # Reconnect after 1 hour
)

# Create a configured "Session" class
SessionLocal = scoped_session(sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
))

# Base class for declarative models
Base = declarative_base()
Base.query = SessionLocal.query_property()

def get_db():
    """
    Dependency that creates a new database session for each request
    and closes it after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()