from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from myenv.db import get_db
from sqlmodel import TaskModel

router = APIRouter(prefix="/patients_data")

class TaskCreate(BaseModel):
    name: str
    age: int
    is_active: bool = False


@router.post("/create")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task