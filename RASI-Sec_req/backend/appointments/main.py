from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from schemas import (Service,Appointment,Doctor)
from models import (Base,services,appointments,doctors)

app = FastAPI()

db_user = "monitoring_user"
db_pass = "isis2503"
db_host = "10.128.0.6"
db_port = "5432"
db_name = "monitoring_db"
 
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
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
# GET 
@app.get("/health/")
def healthCheck():
    return 'ok'
# GET ALL

@app.get("/services", response_model=List[Service])
def getServices():
    with engine.connect() as c:
        stmt = services.select()
        result = c.execute(stmt).all()
        return result



@app.get("/appointments", response_model=List[Appointment])
def getAppointments():

    with engine.connect() as c:
        stmt = appointments.select()
        result = c.execute(stmt).all()
        return result
    
@app.get("/appointments/services/{id}", response_model=List[Appointment])
def getAppointmentByService(id: int, date: str = None, time: str = None):
    with engine.connect() as c:
        stmt = appointments.select().where((appointments.c.service_id == id) & (appointments.c.patient_id.is_(None)))
        if date:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            stmt = stmt.where(appointments.c.date == date_obj)
        if time:
            time_obj = datetime.strptime(time, "%H:%M").time()
            stmt = stmt.where(appointments.c.time == time_obj)
            
        result = c.execute(stmt).all()
        return result

@app.get("/appointments/services", response_model=List[Appointment])
def getAppointmentByServiceName(speciality: str , date: str = None, time: str = None):
    with engine.connect() as c:
        stmt = services.select().where(services.c.speciality == speciality )
        result = c.execute(stmt).fetchone()
        if result is not None:

            fin  =  result[0]
            stmt = appointments.select().where((appointments.c.service_id == fin) & (appointments.c.patient_id.is_(None)))
            if date:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                stmt = stmt.where(appointments.c.date == date_obj)
            if time:
                time_obj = datetime.strptime(time, "%H:%M").time()
                stmt = stmt.where(appointments.c.time == time_obj)

            result = c.execute(stmt).all()
            return result
        return []
# GET ONE

@app.get("/appointments/{id}", response_model=Appointment)
def getAppointment(id: int):
    with engine.connect() as c:
        stmt = appointments.select().where(appointments.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return result


@app.get("/services/{id}", response_model=Service)
def getService(id: int):
    with engine.connect() as c:
        stmt = services.select().where(services.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Service not found")
        return result


# POST
@app.post("/services")
def addService(service: Service):
    serviced = {"id": service.id, "speciality": service.speciality}
    with engine.connect() as c:
        try:
            getService(service.id)
            return "Cannot create Service, already exists"
        except HTTPException as e:
            try:
                c.execute(services.insert().values(serviced))
                c.commit()
                return serviced
            except Exception as e:
                return "Service already exists"


@app.post("/appointments")
def addAppointment(appointment: Appointment):
    appointmentd = {
        "id": appointment.id,
        "date": appointment.date,
        "time": appointment.time,
        "duration": appointment.duration,
        "address": appointment.address,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "service_id": appointment.service_id,
    }
    with engine.connect() as c:
        try:
            getAppointment(appointment.id)
            
            return "Cannot create appointment"
        except HTTPException as e:
            try:
     
                getService(appointment.service_id)
                c.execute(appointments.insert().values(appointmentd))
                c.commit()
                return appointmentd
            except Exception as e:
                return "No se logro nada"


# UPDATE
@app.put("/services/{id}")
def updateService(id: int, service: Service):
    serviced = {"speciality": service.speciality}
    with engine.connect() as c:
        try:
            getService(id)
            c.execute(services.update().where(services.c.id == id).values(**serviced))
            c.commit()
            return serviced
        except HTTPException as e:
            return "Service does not exist"


@app.put("/appointments/{id}")
def updateAppointment(id: int, appointment: Appointment):
    appointmentd = {
        "date": appointment.date,
        "time": appointment.time,
        "duration": appointment.duration,
        "address": appointment.address,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "service_id": appointment.service_id,
    }
    with engine.connect() as c:
        try:
            getAppointment(id)
            c.execute(
                appointments.update()
                .where(appointments.c.id == id)
                .values(**appointmentd)
            )
            c.commit()
            return appointmentd
        except HTTPException as e:
            return "Appointment does not exist"


# DELETE
@app.get("/doctors/{id}", response_model=Doctor)
def getDoctor(id: int):
    with engine.connect() as c:
        stmt = doctors.select().where(doctors.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return result



@app.delete("/appointments/{id}")
def deleteAppointment(id: int):
    with engine.connect() as c:
        stmt = appointments.delete().where(appointments.c.id == id)
        result = c.execute(stmt)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Appointment not found")
        c.commit()
        return {"message": "Appointment deleted successfully"}


@app.delete("/services/{id}")
def deleteService(id: int):
    with engine.connect() as c:
        stmt = services.delete().where(services.c.id == id)
        result = c.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Service not found")
        c.commit()
        return {"message": "Service deleted successfully"}


@app.get("/")
def root():
    with engine.connect() as c:
        return "Microservicio de citas medicas"
