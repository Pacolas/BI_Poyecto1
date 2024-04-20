from fastapi import FastAPI, HTTPException, Path, UploadFile, File, Form,Query
from sqlalchemy import create_engine, text, insert, select
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from hashlib import sha256
from typing import List
from fastapi.responses import FileResponse, Response
import backend_old.model.predict as pr
import pandas as pd 
import io 
import backend_old.model.training as ml
from backend_old.schemas import (
    Training,
    Prediction,
    Metric,
    Version
)
from backend_old.models import (
    trainings,
    predictions,
    metrics,
    Base,
    versions
)

app = FastAPI()

db_user = "admin"
db_pass = "password"
db_host = "localhost"
db_port = "5432"
db_name = "biproyect"


engine = create_engine(
    f"postgresql+psycopg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}", echo=True
)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# # GET 

# GET ALL
@app.get("/predictions", response_model=List[Prediction])
def getPredictions():
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM predictions"))
        return result.all()
@app.get("/metrics", response_model=List[Metric])
def getMetrics():
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM metrics"))
        return result.all()
    
@app.get("/trainings", response_model=List[Training])
def getTrainings(): 
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM trainings"))
        return result.all()
 


# POST
@app.post("/predictions")
def addPrediction(prediction: Prediction):

    predictiond = {
        "creator": prediction.creator,
        "description": prediction.description,
        "calification": prediction.calification,
        'version' : prediction.version
        }
    with engine.connect() as c:
        try:
            getPrediction(prediction.id)
            return "Cannot create Prediction, already exists"
        except HTTPException as e:
            c.execute(predictions.insert().values(predictiond))
            c.commit()
            return predictiond


def getPrediction(id: int):
    with engine.connect() as c:
        stmt = predictions.select().where(predictions.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return result
    
@app.get("/predictions/{version}", response_model=List[Prediction])
def getPredictionByVersion(version: str):
    with engine.connect() as c:
        stmt = predictions.select().where(predictions.c.version == version)
        result = c.execute(stmt).all()
        if result is None:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return result  
@app.post("/trainings")
def addTraining(training: Training):
    
    trainingd = {
        "description": training.description,
        "calification": training.calification,
        'version' : training.version
        }
    
    with engine.connect() as c:
        try:
            getTraining(training.id)
            return "Cannot create Prediction, already exists"
        except HTTPException as e:
            c.execute(trainings.insert().values(trainingd))
            c.commit()
            return trainingd 
@app.post("/versions")
def addVersion(version: Version):
    
    versiond = {
        "name": version.name
        }
    
    with engine.connect() as c:
        try:
            getVersionByName(version.name)
            return "Cannot create Version, already exists"
        except HTTPException as e:
            c.execute(versions.insert().values(versiond))
            c.commit()
            return versiond 

def getVersionByName(name):
    
    with engine.connect() as c:
        stm = versions.select().where(versions.c.name == name)
        result = c.execute(stm ).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Version not found")
        return result

@app.get('/versions', response_model=List[Version])
def getVersions():
    with engine.connect() as c:
        result = c.execute(text("SELECT * FROM versions"))
        return result.all()


@app.post("/trainings/several")
def addTrainings(trainings: List[Training]):
    with engine.connect() as c:
        try:
            stm = versions.select().where(versions.c.name == trainings[0].version)
            result = c.execute(stm ).fetchone()
            if result is None:
                c.execute(versions.insert().values(name=trainings[0].version))
                c.commit()
            for training in trainings:
                addTraining(training)  
            return {"message": "Trainings added successfully"}
        except HTTPException as e:

            return "Error: " + str(e)
@app.post("/predictions/several")
def addPredictions (predictions: List[Prediction]):
    with engine.connect() as c:
        try:
            for predict in predictions:
                addPrediction(predict)  
            return {"message": "Predictions added successfully"}
        except HTTPException as e:
            return "Error: " + str(e)
@app.get("/training/{id}", response_model=Training)
def getTraining(id: int):
    with engine.connect() as c:
        stmt = trainings.select().where(trainings.c.id == id)
        result = c.execute(stmt).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Training not found")
        
        return result



@app.get("/train/{version}")
def train(version: str):
    with engine.connect() as c:
        state = trainings.select().where(trainings.c.version == version )
        result = c.execute(state).all()
        
        df = ml.sqltoDF(result)
        metrics = ml.train_model(df)
        for metric in metrics:
            addMetric(metric,metrics[metric],  version)

        return []


def addMetric(name,value, version):
    data ={'name': name, 'percent': value, 'version':version }
    with engine.connect() as c:
        try:
            c.execute(metrics.insert().values(data))
            c.commit()
            return data
        except HTTPException as e:
            return "Cannot create Version, already exists"
            
                        
@app.get("/metrics/{version}", response_model=List[Metric])
def getMetricsFromVersion(version):
    with engine.connect() as c:
        stmt = metrics.select().where(metrics.c.version == version)
        result = c.execute(stmt).all()
        if result is None:
            raise HTTPException(status_code=404, detail="Metrics not found")
        
        return result


@app.get("/metrics/{name}/matrix")
async def get_image(name: str):
    with engine.connect() as c:
        stm = versions.select().where(versions.c.name == name)
        result = c.execute(stm).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Image not found")
        image_path = f"./backend_old/model/ml_models/mtz_confussion/confusion_matrix{name}.png"
        
        return FileResponse(image_path, media_type="image/png")

@app.get("/wordcloud/{version}/{Class}")
async def getWordCloud(version: str, Class: str):
    
    with engine.connect() as c:
        stm = versions.select().where(versions.c.name == version)
        result = c.execute(stm).fetchone()
        if result is None or Class not in ['1','2','3','4','5']:
            raise HTTPException(status_code=404, detail="Image not found")
        image_path = f"./backend_old/model/ml_models/wordclouds/WordCloud_{version}_{Class}.png"
        img =  FileResponse(image_path, media_type="image/png")
        return img
    
@app.post("/upload/predict")
async def upload_predict_csv(csv_file: UploadFile = File(...), version: str = Form(...)):
    try:
        df = pd.read_csv(csv_file.file)
        df['version'] = version
        df['id'] = None
        df['creator'] = 'Carlos Analista'
        prediction = pr.predict(df, version)
        df['Class'] = prediction
        csv_ret = df.copy()[['Review','Class']].to_csv( index=False)
        df.rename(columns={"Review": "description", "Class": "calification"}, inplace=True)
        data_json = df.to_dict(orient='records')
        xd = [Prediction(**item) for item in data_json]
        addPredictions(xd)  # Convertir cada dict a objeto Training y pasarlos a addTrainings
        
        # Retornar el archivo CSV convertido como un string
        print('Logrado')
        return Response(content=csv_ret, media_type="text/csv")
    except Exception as e:
        print(e)
        return {"error": str(e)}
    

@app.post("/upload")
async def upload_csv(csv_file: UploadFile = File(...), version: str = Form(...)):
    try:
        df = pd.read_csv(csv_file.file)
        df.rename(columns={"Review": "description", "Class": "calification"}, inplace=True)
        df['version'] = version
        df['id'] = None
        data_json = df.to_dict(orient='records')
        xd = [Training(**item) for item in data_json]
        addTrainings(xd)  # Convertir cada dict a objeto Training y pasarlos a addTrainings
        train(version)
        return {"message": "Archivo CSV procesado exitosamente"}
    except Exception as e:
        
        return {"error": str(e)}
    
@app.post("/predict/quotes")
async def predict_text(version: str = Query(...), texto: str = Query(...)):
    try:
        df = pd.DataFrame({'Review': [texto]})
        df['version'] = version
        df['id'] = None
        df['creator'] = "Diego Peruano"
        prediction = pr.predict(df, version)
        df['Class'] = prediction
        df.rename(columns={"Review": "description", "Class": "calification"}, inplace=True)
        data_json = df.to_dict(orient='records')
        xd = [Prediction(**item) for item in data_json]
        addPrediction(xd[0])
        return {"message": "La calificación asignada es " + str(prediction[0])}
    except Exception as e:
        print(e)
        return {"error": str(e)}
@app.get('/classified/{version}')
def getCSVClass(version: str):
    with engine.connect() as c:
        stm = predictions.select().where(predictions.c.version == version)
        result = c.execute(stm).all()
        df = pd.DataFrame(result)[['description', 'calification']]
        df.rename(columns={"description": "Review", "calification": "Class"}, inplace=True)
        csv_string = df.to_csv(index=False)
        
        return Response(content=csv_string, media_type="text/csv")


@app.get("/")
def root():
    with engine.connect() as c:
        postgresql_version = c.execute(text("SELECT version()")).fetchone()[0]
        return ["Hello world", {"postgres_version": postgresql_version}]
