from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#DB_CONNECTION_URL = "postgresql://postgres:passod@localhost:5432/database_name"
#DB_CONNECTION_URL = "postgresql://postgres:280230@localhost:5432/localhost"


DB_CONNECTION_URL = "postgresql+psycopg2://postgres:280230@localhost:5432/postgres"


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

