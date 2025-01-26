from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL')

# Explicitly handle Turso LibSQL URL
sqlite_path = DATABASE_URL.split('//')[1].split('.')[0] + '.db'

engine = create_engine(f'sqlite:///{sqlite_path}', 
                       connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Ensure tables are created
Base.metadata.create_all(bind=engine, checkfirst=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()