from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from myenv.db import get_db
from sqlmodel import TaskModel

router = APIRouter(prefix="/patients_data")


class PatientCreate(BaseModel):
    id: str
    name: str
    age: int
    address: str | None = None
    gender: str | None = None
    height: float | None = None
    weight: float | None = None
    verdict: str | None = None
    phone: str | None = None
    bmi: float | None = None


def patient_to_dict(patient: PatientCreate) -> dict:
    if hasattr(patient, "model_dump"):  # Pydantic 2
        return patient.model_dump()
    return patient.dict()  # Pydantic 1


@router.post("/create")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = TaskModel(**patient_to_dict(patient))
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@router.post("/create/bulk")
def create_patients(
    patients: list[PatientCreate],
    db: Session = Depends(get_db),
):
    new_patients = [TaskModel(**patient_to_dict(patient)) for patient in patients]
    db.add_all(new_patients)
    db.commit()

    for patient in new_patients:
        db.refresh(patient)

    return new_patients