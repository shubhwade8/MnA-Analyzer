import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Default to SQLite for local dev to avoid needing Postgres running
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ma_deals.db")

# Provide connect_args for SQLite
engine = create_engine(
	DATABASE_URL,
	pool_pre_ping=True,
	connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def init_db() -> None:
	from .models.models import Base as ModelsBase
	ModelsBase.metadata.create_all(bind=engine)
