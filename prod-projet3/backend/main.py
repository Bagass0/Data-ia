from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from prediction_service import predict_house_price, get_sample_predictions

# Création de l'application FastAPI
app = FastAPI(
    title="API de Prédiction de Prix de Maison",
    description="API pour prédire le prix d'une maison basée sur ses caractéristiques",
    version="1.0.0"
)

# Modèle Pydantic pour les données d'entrée
class HouseFeatures(BaseModel):
    size: float
    nb_rooms: int
    garden: int

# Modèle Pydantic pour la réponse de prédiction
class PredictionResponse(BaseModel):
    size: float
    nb_rooms: int
    garden: int
    predicted_price: float

@app.get("/")
async def root():
    """Route de base pour vérifier que l'API fonctionne"""
    return {
        "message": "API de Prédiction de Prix de Maison", 
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Route de vérification de santé de l'API"""
    return {"status": "healthy", "service": "prediction-api"}

@app.get("/predictions/samples", response_model=List[PredictionResponse])
async def get_sample_predictions_endpoint():
    """Retourne des prédictions d'exemple codées en dur"""
    return get_sample_predictions()

@app.post("/predict", response_model=PredictionResponse)
async def predict_price(house: HouseFeatures):
    """
    Prédit le prix d'une maison basé sur ses caractéristiques
    """
    predicted_price = predict_house_price(
        size=house.size,
        nb_rooms=house.nb_rooms,
        garden=house.garden
    )
    
    return PredictionResponse(
        size=house.size,
        nb_rooms=house.nb_rooms,
        garden=house.garden,
        predicted_price=predicted_price
    )

@app.get("/predictions/example")
async def get_example_prediction():
    """Retourne un exemple de prédiction simple"""
    return {
        "example_house": {
            "size": 120,
            "nb_rooms": 3,
            "garden": 1
        },
        "predicted_price": predict_house_price(120, 3, 1),
        "message": "Exemple de prédiction pour une maison de 120m² avec 3 chambres et un jardin"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
