import joblib
import backend_old.model.preprocessing as prep

def predict(dataframe, version):
    prep.download_nltk_resources()
    prep.predict_process(dataframe)
    model = joblib.load( "./backend_old/model/ml_models/trained/"+ version +'.pkl')
    return model.predict(dataframe['words'])

