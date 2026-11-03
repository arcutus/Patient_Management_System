from sqlalchemy import Column,Integer,String,Boolean,Float,ForeignKey
from myenv.db import Base
import uuid

class TaskModel(Base):
    __tablename__= "patients"
    id = Column(
        String, 
        primary_key=True, 
        index=True, 
        default=lambda: f"P-{uuid.uuid4().hex[:6].upper()}"
    )
    name = Column(String)
    age = Column(Integer)
    is_active = Column(Boolean, default=False)
    address = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    verdict = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    bmi = Column(Float, nullable=True)
    