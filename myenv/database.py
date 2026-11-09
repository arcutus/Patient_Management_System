import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load environment variables from .env in project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

DB_CONNECTION_URL = os.getenv("DATABASE_URL") or os.getenv("DB_CONNECTION_URL")
if not DB_CONNECTION_URL:
    raise RuntimeError(
        "Missing required environment variable: DATABASE_URL (or DB_CONNECTION_URL) in .env file."
    )

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "Missing required environment variable: SECRET_KEY in .env file."
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")

raw_exp_time = os.getenv("EXP_TIME") or os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
try:
    EXP_TIME = int(raw_exp_time)
except ValueError:
    raise RuntimeError("EXP_TIME must be an integer representing minutes.")

engine = create_engine(DB_CONNECTION_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
