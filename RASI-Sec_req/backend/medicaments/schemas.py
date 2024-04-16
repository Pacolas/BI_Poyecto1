from pydantic import BaseModel, ConfigDict
from datetime import time, date
from typing import Optional

# Schemas



class IPS(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    pnumber: int
    email: str
    address: str


class Medicament(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    brand: str
    quantity: float
    unit: int
    ingredients: str
    contains: int


class Medicament_avaliable(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id_ips: int
    id_medicament: int
    avaliable: int
    price: float


class MedicamentDetail(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    brand: str
    quantity: float
    unit: int
    ingredients: str
    contains: int
    avaliable: int
    price: float

class Log(BaseModel):
    model_config: ConfigDict(from_attributes=True)
    id: int
    name: str
    action: str
    datetime: str
    medicament_id: float

