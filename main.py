from fastapi import APIRouter, FastAPI, Path as FastAPIPath, HTTPException, Query, Depends
from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Annotated,Literal,Optional 
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from myenv.db import Base, engine, get_db
from sqlmodel import TaskModel
from router import router as task_router


Base.metadata.create_all(engine)

app=FastAPI(title="Patient Management Application")
main_router = APIRouter(prefix="/patient_info")

app.include_router(task_router)
app.include_router(main_router)


@main_router.get("/db-check")
def db_check():
    with engine.connect() as connection:
        return {"database": connection.execute(text("SELECT current_database()")).scalar()}



class Patient(BaseModel):
    name: str
    id: Annotated[str, Field(description="Unique identifier for the patient", example="BE26CS188")]
    age: Annotated[int, Field(gt=0, lt=120, description="Age of the patient", example=19)]
    gender: Annotated[Literal["male", "female","other"], Field(description="Gender of the patient", example="female")]

    #literal is used to specify that the gender field can only take one of the specified values: "male", "female", or "other". This ensures that the gender field is validated against these specific options when creating or updating a patient record.
    #annotated is used to provide additional metadata for the fields in the Patient model. It allows you to specify constraints, descriptions, and examples for each field, which can be useful for documentation and validation purposes.
    address: Annotated[str, Field(description="Address of the patient", example="123 Main St")]
    phone: Annotated[str, Field(description="Phone number of the patient", example="555-1234")]
    height: Annotated[float, Field(gt=0, description="Height of the patient in meters", example=1.75)]
    weight: Annotated[float, Field(gt=0,lt=500, description="Weight of the patient in kilograms", example=70.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=self.weight/(self.height**2)
        return round(bmi,2)

    @computed_field
    @property
    def verdict(self) ->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"


#NOTE NOTE using put now

class UpdatePatient(BaseModel): #NOTE UpaatePatient is a pydatic model
    name: Annotated[Optional[str], Field(description="Name of the patient", example="John Doe")] = None
    age: Annotated[Optional[int], Field(gt=0, lt=120, description="Age of the patient", example=19)] = None
    gender: Annotated[Optional[Literal["male", "female","other"]], Field(description="Gender of the patient", example="female")] = None
    address: Annotated[Optional[str], Field(description="Address of the patient", example="123 Main St")] = None
    phone: Annotated[Optional[str], Field(description="Phone number of the patient", example="555-1234")] = None
    height: Annotated[Optional[float], Field(gt=0, description="Height of the patient in meters", example=1.75)] = None
    weight: Annotated[Optional[float], Field(gt=0,lt=500, description="Weight of the patient in kilograms", example=70.5)] = None

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, value):
        return value.casefold() if isinstance(value, str) else value





#NOTE NOTE @ is used to create endpoints in FastAPI. It is a decorator that is used to define a route for the API. The @app.get("/") decorator specifies that the function hello() should be called when a GET request is made to the root endpoint ("/") of the API.

@main_router.get("/")# this here refers to the root endpoint of the API
def hello ():
    return {"message":"Patients Management API"}#here a dictionary is being returned with a key "message" and a value "Hello, World!" when the hello() function is called. This will be the response sent back to the client when they make a GET request to the root endpoint of the API.

#first hello world api
@main_router.get('/about')# this here refers to the /about endpoint of the API
#if anyone makes a GET request to the /about endpoint, the about() function will be called and it will return a dictionary with a key "message" and a value "This is an example of a FastAPI application." This will be the response sent back to the client.
def about():
    return {"message":"A fully functional API to manage patient's records"}


@main_router.get('/view')# this here refers to the /view_patients endpoint of the API
def view_patients(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()


@main_router.get('/patient/{name}')
def view_patient(
    name: str = FastAPIPath(
        ..., 
        description='name of pateint must not be empty or have any other char orther than engish alphabets',
        examples={'default': {'summary': 'Example patient name', 'value': 'John Doe'}},
    ),
    db: Session = Depends(get_db),
):
    requested_name = ''.join(name.split()).casefold()
    for patient in db.query(TaskModel).all():
        patient_name = ''.join((patient.name or '').split()).casefold()
        if patient_name == requested_name:
            return patient
    raise HTTPException(status_code=404, detail='Patient not found')

@main_router.get('/patient/id/{patient_id}')
def view_patient_by_id(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(TaskModel, patient_id)
    if patient is not None:
        return patient
    raise HTTPException(status_code=404, detail='Patient not found')

@main_router.get('/sort')# this here refers to the /sort endpoint of the API
def sort_patients(
    sort_by: str = Query(..., description='sort by name, age, or gender'),
    order: str = Query('asc', description='sort in ascending or descending order'),
    db: Session = Depends(get_db),
):
    if sort_by not in ['name', 'age', 'gender']:
        raise HTTPException(status_code=400, detail='Invalid field to sort by. Must be one of name, age, gender')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Order must be either asc or desc')

    data = db.query(TaskModel).all()
    sorted_data = sorted(data, key=lambda patient: str(getattr(patient, sort_by, '')).lower())
    if order == 'desc':
        sorted_data.reverse()
    return sorted_data

@main_router.post('/create')# this here refers to the /create endpoint of the API
def create_patient(patient: Patient, db: Session = Depends(get_db)):
    if db.get(TaskModel, patient.id) is not None:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists')
    db_patient = TaskModel(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return JSONResponse(
        status_code=201,
        content={
            'message': 'Patient created successfully',
            'patient': patient.model_dump(),
        },
    )

@main_router.put('/edit/{patient_id}')# this here refers to the /edit endpoint of the API
def edit_patient(
    patient_id: str,
    patient_update: UpdatePatient,
    db: Session = Depends(get_db),
):
    patient = db.get(TaskModel, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail='incorrect patient id')

    updated_fields = patient_update.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in updated_fields.items():
        setattr(patient, field, value)

    if patient.height is not None and patient.weight is not None:
        height_in_meters = patient.height / 100 if patient.height > 3 else patient.height
        patient.bmi = round(patient.weight / (height_in_meters ** 2), 2)
        if patient.bmi < 18.5:
            patient.verdict = 'Underweight'
        elif patient.bmi < 25:
            patient.verdict = 'Normal weight'
        elif patient.bmi < 30:
            patient.verdict = 'Overweight'
        else:
            patient.verdict = 'Obesity'

    db.commit()
    db.refresh(patient)
    return {'message': 'patient updated', 'patient': patient}

#for delete
@main_router.delete('/delete/{patient_id}')
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(TaskModel, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail='patient not found')
    db.delete(patient)
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'patient deleted'})
        
        
