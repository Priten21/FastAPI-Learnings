from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

app = FastAPI(title="Patient Records API", description="Mini project to manage patient records", version="1.0")

# Patient Model
class Patient(BaseModel):
    id: int
    name: str = Field(..., max_length=50)
    email: EmailStr
    age: int = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    disease: Optional[str] = None

# In-Memory Database
patients_db: List[Patient] = []

# Create Patient (POST)
@app.post("/patients/", response_model=Patient)
def add_patient(patient: Patient):
    # Check duplicate ID
    for p in patients_db:
        if p.id == patient.id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    patients_db.append(patient)
    return patient

# Get All Patients (GET)
@app.get("/patients/", response_model=List[Patient])
def get_all_patients():
    return patients_db

# Get Patient by ID (GET)
@app.get("/patients/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    for patient in patients_db:
        if patient.id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

# Update Patient (PUT)
@app.put("/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, updated_patient: Patient):
    for index, patient in enumerate(patients_db):
        if patient.id == patient_id:
            patients_db[index] = updated_patient
            return updated_patient
    raise HTTPException(status_code=404, detail="Patient not found")

# Delete Patient (DELETE)
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for index, patient in enumerate(patients_db):
        if patient.id == patient_id:
            patients_db.pop(index)
            return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")
