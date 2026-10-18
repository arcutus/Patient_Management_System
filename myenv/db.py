from sqlalchemy.orm import sessionmaker, declarative_base
from myenv.database import engine

Base = declarative_base()
localsession=sessionmaker(bind=engine)

def get_db():
    session=localsession ()
    try:
        yield session
    finally:
        session.close()