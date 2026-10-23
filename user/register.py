import uuid

from sqlalchemy import Column, String
from myenv.db import Base

class UserModel(Base):
    __tablename__="user_table"

    id = Column(
        String,
        primary_key=True,
        default=lambda: f"U-{uuid.uuid4().hex.upper()}",
    )
    name=Column(String)
    username=Column(String,nullable=False)
    hash_password=Column(String,nullable=False)
    email=Column(String)
    

