import joblib
import pandas as pd
import os

# Chargement du modèle une seule fois au démarrage du module
def load_model():
    """Charge le modèle de machine learning"""
    model_path = os.path.join("assets", "regression.joblib")
    
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        raise FileNotFoundError(f"Le modèle n'a pas été trouvé à : {model_path}")

# Chargement du modèle au niveau du module
MODEL = load_model()

def predict_house_price(size: float, nb_rooms: int, garden: int) -> float:
    """
    Fonction de prédiction de prix de maison utilisant le modèle ML
    
    Args:
        size: Taille de la maison en m²
        nb_rooms: Nombre de chambres
        garden: Présence d'un jardin (0 = non, 1 = oui)
    
    Returns:
        Prix prédit de la maison en euros
    """
    # Préparation des données pour le modèle
    input_data = pd.DataFrame({
        'size': [size],
        'nb_rooms': [nb_rooms],
        'garden': [garden]
    })
    
    # Prédiction avec le modèle ML
    prediction = MODEL.predict(input_data)
    
    return float(prediction[0])


def get_sample_predictions():
    """
    Retourne une liste de prédictions d'exemple
    """
    sample_predictions = [
        {
            "size": 100,
            "nb_rooms": 3,
            "garden": 1,
            "predicted_price": predict_house_price(100, 3, 1)
        },
        {
            "size": 80,
            "nb_rooms": 2,
            "garden": 0,
            "predicted_price": predict_house_price(80, 2, 0)
        },
        {
            "size": 150,
            "nb_rooms": 4,
            "garden": 1,
            "predicted_price": predict_house_price(150, 4, 1)
        }
    ]
    
    return sample_predictions
