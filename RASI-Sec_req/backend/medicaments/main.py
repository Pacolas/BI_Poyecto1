from fastapi import FastAPI, HTTPException, Path
from sqlalchemy import create_engine, text
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from schemas import (
    IPS,
    Medicament_avaliable,
    Medicament,
    MedicamentDetail,Log
)
from models import (
    ips,Base,
    med_avaliability,
    medicaments,log
)

app = FastAPI()

db_user = "monitoring_user"
db_pass = "isis2503"
db_host = "10.182.0.2"
db_port = "5432"
db_name = "monitoring_db"

 
engine = create_engine(
    f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}", echo=True
)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
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
    return '"ok'
# GET ALL

@app.get("/medicaments", response_model=List[Medicament])
def getMedicaments():
    with engine.connect() as c:
        stmt = medicaments.select()
        result = c.execute(stmt)
        return result.all() 
    
@app.get("/logs", response_model=List[Log])
def getLogs():
    with engine.connect() as c:
        stmt = log.select()
        result = c.execute(stmt)
        return result.all() 


# GET ONE

@app.get("/ips/{id}", response_model=IPS)
def getIPS(id: int):
    with engine.connect() as c:
        stmt = ips.select().where(ips.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="IPS not found")
        return result


@app.get("/medicaments/{id}", response_model=Medicament)
def getMedicament(id: int):
    with engine.connect() as c:
        stmt = medicaments.select().where(medicaments.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Medicament not found")
        return result


@app.get("/ips/{id_ips}/medicaments", response_model=List[MedicamentDetail])
def getMedsAvaliability(id_ips: int):
    with engine.connect() as c:
        stmt = (
            "SELECT * FROM medicaments_avaliable  LEFT JOIN MEDICAMENTS ON MEDICAMENTS.ID = medicaments_avaliable.ID_MEDICAMENT  WHERE id_ips = "
            + str(id_ips)
        )
        result = c.execute(text(stmt)).all()

        return result


@app.get("/ips/{id_ips}/medicaments/{id_medicament}", response_model=MedicamentDetail)
def getMedAvaliability(id_ips: int, id_medicament: int):
    with engine.connect() as c:
        stmt = (
            "SELECT * FROM medicaments_avaliable  LEFT JOIN MEDICAMENTS ON MEDICAMENTS.ID = medicaments_avaliable.ID_MEDICAMENT  WHERE id_ips = "
            + str(id_ips)
            + " AND id_medicament = "
            + str(id_medicament)
        )
        result = c.execute(text(stmt)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Medicament not found")
        return result


@app.get("/medicaments/{id_medicament}/ips", response_model=IPS)
def getMedIPS(id_medicament: int):
    with engine.connect() as c:
        stmt = (
            "SELECT * FROM medicaments_avaliable  LEFT JOIN IPS ON IPS.ID = medicaments_avaliable.ID_IPS  WHERE id_medicament = "
            + str(id_medicament)
        )
        result = c.execute(text(stmt)).fetchone()
        return result


# POST
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


@app.post("/medicaments")
def addMedicament(medicament: Medicament):
    medicamentd = {
        "id": medicament.id,
        "name": medicament.name,
        "brand": medicament.name,
        "quantity": medicament.quantity,
        "unit": medicament.unit,
        "ingredients": medicament.ingredients,
        "contains": medicament.contains,
    }
    with engine.connect() as c:
        try:
            addLog(medicamentd['id']-1,medicamentd['id'] )
            getMedicament(medicament.id)
            return "Cannot create Medicament, already exists"
        except HTTPException as e:
        
            c.execute(medicaments.insert().values(medicamentd))
            c.commit()
            return medicamentd
        

def addLog(id, medicament_id):
    
    logd = {
        "id": id,
        "name": "Nicolas Lopez Junco",
        'action': "Just added a new medicament",
        "datetime": "2020-10-10 10:55",
        "medicament_id": medicament_id
    }
    with engine.connect() as c:
        try:
            getLog(id)
            return "Cannot create Log, already exists"
        except HTTPException as e:
            c.execute(log.insert().values(logd))
            c.commit()
            return logd
        
@app.get("/logs/{id}", response_model=Log)
def getLog(id: int):
    with engine.connect() as c:
        stmt = log.select().where(log.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Log not found")
        return result

@app.post("/ips/{id_ips}/medicaments")
def addMedicamentIPS(
    mavaliable: Medicament_avaliable,
    id_ips: int = Path(..., title="ID of the IPS in the URL"),
):
    medicamentd = {
        "id_ips": id_ips,
        "id_medicament": mavaliable.id_medicament,
        "avaliable": mavaliable.avaliable,
        "price": mavaliable.price,
    }
    with engine.connect() as c:
        try:
            getMedAvaliability(id_ips, mavaliable.id_medicament)
            return "Cannot create Medicament, already exists"
        except HTTPException:
            try:
                getMedicament(mavaliable.id_medicament)
                getIPS(id_ips)
                c.execute(med_avaliability.insert().values(medicamentd))
                c.commit()
                return medicamentd
            except Exception:
                return HTTPException(
                    status_code=404, detail="IPS or Medicament does not exists."
                )


@app.get("/")
def root():
    with engine.connect() as c:
        postgresql_version = c.execute(text("SELECT version()")).fetchone()[0]
        return ["Hello world", {"postgres_version": postgresql_version}]
