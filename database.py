from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import libsql_client

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# PostgreSQL Configuration
if 'postgresql' in DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Add SSL requirement for Neon
    if "?" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"
    elif "sslmode=" not in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

# LibSQL Configuration
elif 'libsql' in DATABASE_URL:
    # Use SQLite as the base dialect
    sqlite_url = f"sqlite:///libsql_database.db"
    
    # Create a separate libsql client for actual database operations
    libsql_client_instance = libsql_client.create_client(url=DATABASE_URL)
    
    engine = create_engine(sqlite_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
else:
    raise ValueError("Unsupported database type")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()