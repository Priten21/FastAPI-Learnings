from pydantic import BaseModel ,EmailStr, AnyUrl, Field
from typing import List , Dict ,Optional, Annotated

class Patient(BaseModel):

    name : Annotated[str,Field(max_length=50,title='Name of Patient',description='Give the full name of the patient in less than 50 chars',examples=['John Doe','Brad Pitt'])]
    email : EmailStr
    social : AnyUrl
    age : int = Field(gt= 0)
    weight : Annotated[float,Field(gt=0,strict=True)]
    married :Annotated[bool,Field(default=False)]
    allergies : Annotated[Optional[List[str]], Field(default=None,max_length=5)]
    contact_details : Dict[str , str]

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.social)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted')


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.email)
    print(patient.social)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('updated')


patient_info = {'name':'Priten','email':'connectwpriten@gmail.com',
                'social':'http://linkedIn.com/2104','age':20, 'weight':70.5,'allergis':['peanuts','milk','dust','cranberries','pollen'],'contact_details':{'phone':'16042245'}}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)


# patient1 = Patient(**patient_info)
# update_patient_data(patient1)