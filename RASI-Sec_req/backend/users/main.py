from fastapi import FastAPI, HTTPException, Path
from sqlalchemy import create_engine, text
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from hashlib import sha256
from typing import List
from backend.users.schemas import (
    Patient,
    Doctor,
    IPS
)
from backend.users.models import (
    patients,
    doctors,
    ips
)

app = FastAPI()


db_user = "admin"
db_pass = "password"
db_host = "localhost"
db_port = "5432"
db_name = "postgres"

 
engine = create_engine(
    f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}", echo=True
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# GET 
@app.get("/health/")
def healthCheck():
    return 'ok'
# GET ALL
@app.get("/patients", response_model=List[Patient])
def getPatients():
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM patients"))
        return result.all()


@app.get("/ips", response_model=List[IPS])
def getIPSs():
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM ips"))
        return result.all()




@app.get("/doctors", response_model=List[Doctor])
def getDoctors():
    with engine.connect() as c:
        stmt = doctors.select()
        result = c.execute(stmt).all()
        return result


@app.get("/patients/{id}", response_model=Patient)
def getPatient(id: int):
    with engine.connect() as c:
        stmt = patients.select().where(patients.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        return result

@app.get("/ips/{id}", response_model=IPS)
def getIPS(id: int):
    with engine.connect() as c:
        stmt = ips.select().where(ips.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="IPS not found")
        return result







@app.get("/doctors/{id}", response_model=Doctor)
def getDoctor(id: int):
    with engine.connect() as c:
        stmt = doctors.select().where(doctors.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return result



# POST
@app.post("/patients")
def addPatient(patient: Patient):
    print(patient.resume)
    patientd = {
        "id": patient.id,
        "name": patient.name,
        "birth": patient.birth,
        "gender": patient.gender,
        "pnumber": patient.pnumber,
        "email": patient.email,
        "resume": patient.resume,
        "hash" : sha256(patient.resume.encode("utf-8")).hexdigest()
    }
    with engine.connect() as c:
        try:
            getPatient(patient.id)
            return "Cannot create Patient, already exists"
        except HTTPException as e:
            c.execute(patients.insert().values(patientd))
            c.commit()
            return patientd


@app.post("/ips")
def addIPS(ipss: IPS):
    ipsd = {
        "id": ipss.id,
        "name": ipss.name,
        "pnumber": ipss.pnumber,
        "email": ipss.email,
        "address": ipss.address,
    }
    with engine.connect() as c:
        try:
            getIPS(ipss.id)
            return "Cannot create IPS, already exists"
        except HTTPException as e:
            c.execute(ips.insert().values(ipsd))
            c.commit()
            return ipsd



@app.post("/doctors")
def addDoctor(doctor: Doctor):
    doctord = {
        "id": doctor.id,
        "name": doctor.name,
        "birth": doctor.birth,
        "gender": doctor.gender,
        "pnumber": doctor.pnumber,
        "email": doctor.email,
    }
    with engine.connect() as c:
        try:
            getDoctor(doctor.id)
            return "Cannot create Docttor, already exists"
        except HTTPException as e:
            c.execute(doctors.insert().values(doctord))
            c.commit()
            return doctord


# UPDATE
@app.put("/patients/{id}")
def updatePatient(id: int, patient: Patient):
    patientd = {
        "name": patient.name,
        "birth": patient.birth,
        "gender": patient.gender,
        "pnumber": patient.pnumber,
        "email": patient.email,
    }
    with engine.connect() as c:
        try:
            getPatient(id)
            c.execute(patients.update().where(patients.c.id == id).values(**patientd))
            c.commit()
            return patientd
        except HTTPException as e:
            return "Patient does not exist"


@app.put("/doctors/{id}")
def updateDoctor(id: int, doctor: Doctor):
    doctord = {
        "name": doctor.name,
        "birth": doctor.birth,
        "gender": doctor.gender,
        "pnumber": doctor.pnumber,
        "email": doctor.email,
    }
    with engine.connect() as c:
        try:
            getDoctor(id)
            c.execute(doctors.update().where(doctors.c.id == id).values(**doctord))
            c.commit()
            return doctord
        except HTTPException as e:
            return "Doctor does not exist"

# DELETE


@app.delete("/patients/{id}")
def deletePatient(id: int):
    with engine.connect() as c:
        stmt = patients.delete().where(patients.c.id == id)
        result = c.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        c.commit()
        return {"message": "Patient deleted successfully"}


@app.delete("/doctors/{id}")
def deleteDoctor(id: int):
    with engine.connect() as c:
        stmt = doctors.delete().where(doctors.c.id == id)
        result = c.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Doctor not found")
        c.commit()
        return {"message": "Doctor deleted successfully"}


@app.get("/")
def root():
    with engine.connect() as c:
        return "Microservicio de Usuarios"
