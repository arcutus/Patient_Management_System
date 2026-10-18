from sqlalchemy import Column,Integer,String,Boolean
from myenv.db import Base

class TaskModel(Base):
    __tablename__= "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    is_active = Column(Boolean, default=False)
    

