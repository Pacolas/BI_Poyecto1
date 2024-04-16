from pydantic import BaseModel, ConfigDict
from datetime import time, date
from typing import Optional

# Schemas

class Doctor(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    birth: str
    gender: str
    pnumber: int
    email: str



class Appointment(BaseModel):
    id: int
    date: date
    time: time
    duration: int
    address: str
    patient_id: Optional[int]
    doctor_id: int
    service_id: int


class Service(BaseModel):
    id: int
    speciality: str

