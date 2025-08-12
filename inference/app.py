# Segunda solucion usando el framework para backend FastAPI

from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Modelo Pydantic para validación
class Passenger(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str
    HasCabin: int
    FamilySize: int

# Cargar modelo al iniciar
model = joblib.load('/opt/ml/model/model.joblib')

@app.post("/predict")
def predict(passenger: Passenger):
    try:
        # Convertir a DataFrame
        input_data = pd.DataFrame([passenger.dict()])

        # Preprocesamiento (usar mismo pipeline de entrenamiento)
        processed_data = preprocess(input_data)

        # Predecir
        prediction = model.predict(processed_data)
        probability = model.predict_proba(processed_data)[:, 1]

        return {
            "survived": bool(prediction[0]),
            "probability": float(probability[0]),
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
