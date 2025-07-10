def predict_house_price(size: float, nb_rooms: int, garden: int) -> float:
    """
    Fonction de prédiction de prix de maison avec des valeurs codées en dur
    
    Args:
        size: Taille de la maison en m²
        nb_rooms: Nombre de chambres
        garden: Présence d'un jardin (0 = non, 1 = oui)
    
    Returns:
        Prix prédit de la maison en euros
    """
    # Prédictions codées en dur pour l'exemple
    base_price = 150000  # Prix de base
    price_per_sqm = 2000  # Prix par m²
    price_per_room = 25000  # Prix par chambre
    garden_bonus = 50000  # Bonus pour jardin
    
    predicted_price = (
        base_price + 
        (size * price_per_sqm) + 
        (nb_rooms * price_per_room) + 
        (garden * garden_bonus)
    )
    
    return predicted_price


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
