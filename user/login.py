from sqlalchemy import Column,String,Integer,Boolean,DateTime
from myenv.db import Base

class UserModel(Base):
    __tablename__="user_table"

    id=Column(String,primary_key=True)
    name=Column(String)
    username=Column(String,nullable=False)
    hash_password=Column(String,nullable=False)
    email=Column(String)
    


