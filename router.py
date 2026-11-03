from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session
from myenv.db import get_db
from sqlmodel import TaskModel

router = APIRouter(prefix="/data_patient")


class PatientCreate(BaseModel):
    id: str | None = None  # optional
    user_id: str | None = None  # optional link to user_table
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
    data = patient.model_dump() if hasattr(patient, "model_dump") else patient.dict()
    # If id is None, remove it so SQLAlchemy auto-generates it
    if data.get("id") is None:
        data.pop("id", None)
    return data


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
    saved_patients = []
    for patient in patients:
        saved_patients.append(db.merge(TaskModel(**patient_to_dict(patient))))
    db.commit()

    return {
        "message": f"Successfully processed {len(saved_patients)} patient(s)",
        "patients": [
            {
                "id": p.id,
                "user_id": p.user_id,
                "name": p.name,
                "age": p.age,
                "gender": p.gender,
                "address": p.address,
                "phone": p.phone,
                "height": p.height,
                "weight": p.weight,
            }
            for p in saved_patients
        ],
    }


@router.delete("/clear-all")
def clear_all_patients(db: Session = Depends(get_db)):
    deleted_count = db.query(TaskModel).delete()
    db.commit()
    return {"message": f"Cleared {deleted_count} patients from database"}


@router.delete("/delete/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = db.query(TaskModel).filter(TaskModel.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": f"Patient {patient_id} deleted successfully"}


@router.put("/update/{patient_id}")
def update_patient(
    patient_id: str,
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
):
    db_patient = db.query(TaskModel).filter(TaskModel.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for key, value in patient_to_dict(patient_data).items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return {"message": "Patient updated successfully", "patient": patient_data}


@router.get("/view_patients")
def get_task(db: Session = Depends(get_db)):
    task = db.query(TaskModel).all()
    return {"status": "All tasks", "data": task}


@router.get("/patient_data/{patient_id}")
def get_patient_id(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(TaskModel).filter(TaskModel.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Invalid ID")
    return {"status": "Task fetched successfully", "data": patient}
