from pydantic import BaseModel, ConfigDict
from datetime import time, date
from typing import Optional

# Schemas


class Training(BaseModel):

    id: Optional[int]
    description: str
    calification: int
    version: str


class Prediction(BaseModel):

    id: int
    creator: str
    description: str
    calification: int
    version: str


class Metric(BaseModel):
    id: int
    name: str
    percent: float
    version: str

class Version (BaseModel):
    id: Optional[int]
    name:str