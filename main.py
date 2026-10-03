from pathlib import Path
from fastapi import FastAPI, Path as FastAPIPath, HTTPException, Query
import json
from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Annotated,Literal,Optional 
from fastapi.responses import JSONResponse

app = FastAPI()

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





def load_data():
    file_path = Path(__file__).resolve().parent / 'patients.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

#NOTE NOTE @ is used to create endpoints in FastAPI. It is a decorator that is used to define a route for the API. The @app.get("/") decorator specifies that the function hello() should be called when a GET request is made to the root endpoint ("/") of the API.

def save_data(data):
    file_path = Path(__file__).resolve().parent / 'patients.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)



@app.get("/")# this here refers to the root endpoint of the API
def hello ():
    return {"message":"Patients Management API"}#here a dictionary is being returned with a key "message" and a value "Hello, World!" when the hello() function is called. This will be the response sent back to the client when they make a GET request to the root endpoint of the API.

#first hello world api
@app.get('/about')# this here refers to the /about endpoint of the API
#if anyone makes a GET request to the /about endpoint, the about() function will be called and it will return a dictionary with a key "message" and a value "This is an example of a FastAPI application." This will be the response sent back to the client.
def about():
    return {"message":"A fully functional API to manage patient's records"}


@app.get('/view')# this here refers to the /view_patients endpoint of the API
def view_patients():
    data = load_data()# this line calls the load_data() function to load the patient data from the patients.json file and assigns it to the variable data.
    return data# this line returns the patient data as a response to the client when they make a GET request to the /view_patients endpoint of the API.


@app.get('/patient/{name}')
def view_patient(
    name: str = FastAPIPath(
        ..., 
        description='name of pateint must not be empty or have any other char orther than engish alphabets',
        examples={'default': {'summary': 'Example patient name', 'value': 'John Doe'}},
    )
):
    #load all the patients
    data = load_data()# this line calls the load_data() function to load the patient data from the patients.json file and assigns it to the variable data.
    
    requested_name = ''.join(name.split()).casefold()
    for patient in data:
        patient_name = ''.join(patient.get('name', '').split()).casefold()
        if patient_name == requested_name:
            return patient
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/patient/id/{patient_id}')
def view_patient_by_id(patient_id: str):
    data = load_data()
    for patient in data:
        if patient.get('id') == patient_id:
            return patient
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')# this here refers to the /sort endpoint of the API
def sort_patients(
    sort_by: str = Query(..., description='sort by name, age, or gender'),
    order: str = Query('asc', description='sort in ascending or descending order')
):
    if sort_by not in ['name', 'age', 'gender']:
        raise HTTPException(status_code=400, detail='Invalid field to sort by. Must be one of name, age, gender')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Order must be either asc or desc')

    data = load_data()
    sorted_data = sorted(data, key=lambda patient: str(patient.get(sort_by, '')).lower())
    if order == 'desc':
        sorted_data.reverse()
    return sorted_data



@app.post('/create')# this here refers to the /create endpoint of the API
def create_patient(patient: Patient):
    #load existing patients
    data = load_data()
    #to chek if the patient already exists
    if patient.id in [p.get('id') for p in data]:
        raise HTTPException(status_code=400, detail='Patient with this ID already exists')
    # new patitent data to be added 
    
    data.append(patient.model_dump())

    #save into the jason file
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            'message': 'Patient created successfully',
            'patient': patient.model_dump(),
        },
    )

@app.put('/edit/{patient_id}')# this here refers to the /edit endpoint of the API
def edit_patient(patient_id:str,patient_update:UpdatePatient):

    data = load_data()
    for existing_patient_info in data:
        if existing_patient_info.get('id') == patient_id:
            updated_patient_info = patient_update.model_dump(exclude_unset=True, exclude_none=True)
            existing_patient_info.update(updated_patient_info)

            height = existing_patient_info.get('height')
            weight = existing_patient_info.get('weight')
            if height is not None and weight is not None:
                height_in_meters = height / 100 if height > 3 else height
                bmi = round(weight / (height_in_meters ** 2), 2)
                existing_patient_info['bmi'] = bmi
                if bmi < 18.5:
                    existing_patient_info['verdict'] = 'Underweight'
                elif bmi < 25:
                    existing_patient_info['verdict'] = 'Normal weight'
                elif bmi < 30:
                    existing_patient_info['verdict'] = 'Overweight'
                else:
                    existing_patient_info['verdict'] = 'Obesity'

            save_data(data)
            return JSONResponse(
                status_code=200,
                content={'message': 'patient updated', 'patient': existing_patient_info},
            )

    raise HTTPException(status_code=404, detail='incorrect patient id')

#for delete
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    for index, patient in enumerate(data):
        if patient.get('id') == patient_id:
            del data[index]
            save_data(data)
            return JSONResponse(status_code=200, content={'message': 'patient deleted'})

    raise HTTPException(status_code=404, detail='patient not found')
        
        

    

