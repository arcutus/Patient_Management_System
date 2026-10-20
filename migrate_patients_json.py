import json
from pathlib import Path

from sqlalchemy.orm import sessionmaker

from myenv.database import engine
from sqlmodel import TaskModel


def main() -> None:
    json_path = Path(__file__).resolve().parent / "patients.json"
    records = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("patients.json must contain a list of patient records")

    SessionLocal = sessionmaker(bind=engine)
    imported = 0
    skipped = 0

    with SessionLocal() as db:
        existing_ids = {row[0] for row in db.query(TaskModel.id).all()}
        patients = []

        for row_number, record in enumerate(records, start=1):
            if not isinstance(record, dict):
                raise ValueError(f"Record {row_number} in patients.json must be an object")

            patient_id = record.get("id")
            if not isinstance(patient_id, str) or not patient_id.strip():
                raise ValueError(f"Record {row_number} in patients.json needs a non-empty string id")

            if patient_id in existing_ids:
                skipped += 1
                continue

            patients.append(TaskModel(**record))
            existing_ids.add(patient_id)

        db.add_all(patients)
        db.commit()
        imported = len(patients)

    print(f"Imported {imported} patients; skipped {skipped} IDs already in PostgreSQL.")


if __name__ == "__main__":
    main()
