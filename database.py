# database.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Modify the DATABASE_URL for PostgreSQL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Add SSL requirement for PostgreSQL
if "?" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"
elif "sslmode=" not in DATABASE_URL:
    DATABASE_URL += "&sslmode=require"

# Create the SQLAlchemy engine based on the URL scheme
if DATABASE_URL.startswith("postgresql://"):
    engine = create_engine(DATABASE_URL)
elif DATABASE_URL.startswith("libsql://"):
    # Transform libsql URL for Turso to a PostgreSQL compatible format
    turso_url = DATABASE_URL.replace("libsql://", "postgresql://")
    # Append SSL settings
    if "?" not in turso_url:
        turso_url += "?sslmode=require"
    elif "sslmode=" not in turso_url:
        turso_url += "&sslmode=require"
    
    engine = create_engine(turso_url)
else:
    raise ValueError("Unsupported database URL scheme")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✓ Database connection successful!")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False