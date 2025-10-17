from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

# --- 1. Setup the FastAPI App ---
app = FastAPI(
    title="Patient Management API",
    description="A simple API to manage patient records.",
    version="1.0.0",
)

# --- 2. Define Pydantic Models (Data Blueprints) ---

# This model is for creating a new patient (client doesn't send an ID)
class PatientCreate(BaseModel):
    name: str
    age: int
    sex: str
    illness: str

# This model is for the data stored in our "database"
class Patient(PatientCreate):
    id: int

# This model is for updating a patient (all fields are optional)
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    illness: Optional[str] = None


# --- 3. Create an In-Memory "Database" ---
# In a real application, this would be a real database like PostgreSQL or MySQL.
# We'll use a simple list and dictionary for this example.
patients_db: List[Patient] = [
    Patient(id=1, name="John Doe", age=45, sex="Male", illness="Hypertension"),
    Patient(id=2, name="Jane Smith", age=32, sex="Female", illness="Asthma"),
]

# Helper to find patient by ID
def find_patient_by_id(patient_id: int):
    for patient in patients_db:
        if patient.id == patient_id:
            return patient
    return None

# --- 4. Define API Endpoints (CRUD Operations) ---

# CREATE Operation
@app.post("/patients/", response_model=Patient, status_code=201)
def create_patient(patient_data: PatientCreate):
    """
    Adds a new patient to the database.
    """
    new_id = max(p.id for p in patients_db) + 1 if patients_db else 1
    new_patient = Patient(id=new_id, **patient_data.dict())
    patients_db.append(new_patient)
    return new_patient

# READ Operation (Get all patients)
@app.get("/patients/", response_model=List[Patient])
def get_all_patients():
    """
    Retrieves a list of all patients.
    """
    return patients_db

# READ Operation (Get a single patient by ID)
@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    """
    Retrieves a single patient by their unique ID.
    """
    patient = find_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    return patient

# UPDATE Operation
@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient_update: PatientUpdate):
    """
    Updates the details of an existing patient.
    """
    patient = find_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")

    # Get the update data, excluding any fields that weren't set
    update_data = patient_update.dict(exclude_unset=True)
    
    # Update the patient object
    for key, value in update_data.items():
        setattr(patient, key, value)
        
    return patient

# DELETE Operation
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    """
    Deletes a patient from the database by their ID.
    """
    patient = find_patient_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found.")
    
    patients_db.remove(patient)
    return {"status": "success", "message": f"Patient with ID {patient_id} has been deleted."}

# --- 5. How to Run This App ---
#
#    uvicorn patient_management_api:app --reload
#
#    Then, open your browser and go to the interactive docs:
#    http://127.0.0.1:8000/docs
