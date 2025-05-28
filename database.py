from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use SQLite for simplicity. You can switch this to PostgreSQL later if needed.
SQLALCHEMY_DATABASE_URL = "sqlite:///./vehicles.db"

# create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# create a configured "session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for all models
Base = declarative_base()
