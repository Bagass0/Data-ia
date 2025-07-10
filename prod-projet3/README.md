# Projet de Prédiction de Prix de Maison

Ce projet comprend une API FastAPI pour les prédictions et une interface Streamlit qui consomme cette API.

## Architecture du projet

```
prod-projet3/
├── assets/
│   ├── houses.csv              # Dataset d'entraînement
│   ├── regression.joblib       # Modèle ML entraîné
│   └── train_model.py          # Script d'entraînement du modèle
├── backend/                    # (À créer - organisation future)
│   ├── main.py                 # API FastAPI
│   └── prediction_service.py   # Service de prédiction
├── main.py                     # API FastAPI (racine temporaire)
├── prediction_service.py       # Service de prédiction (racine temporaire)
├── model_app.py                # Interface Streamlit
└── requirements.txt            # Dépendances Python
```

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Démarrer l'API FastAPI

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

L'API sera accessible sur : http://127.0.0.1:8000

### 2. Démarrer l'interface Streamlit

```bash
streamlit run model_app.py --server.port 8501
```

L'interface sera accessible sur : http://localhost:8501

## Endpoints de l'API

- `GET /` - Route de base
- `GET /health` - Vérification de santé
- `GET /docs` - Documentation Swagger automatique
- `GET /predictions/samples` - Exemples de prédictions
- `POST /predict` - Prédiction personnalisée

### Exemple d'utilisation de l'API

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"size": 100, "nb_rooms": 3, "garden": 1}'
```

## Fonctionnalités

### Interface Streamlit
- ✅ Connexion automatique à l'API
- ✅ Vérification du statut de l'API
- ✅ Formulaire interactif pour les prédictions
- ✅ Affichage des résultats avec détails
- ✅ Tests de connexion API
- ✅ Exemples de prédictions depuis l'API

### API FastAPI
- ✅ Prédictions en temps réel
- ✅ Documentation automatique
- ✅ Validation des données avec Pydantic
- ✅ Gestion d'erreurs
- ✅ Endpoints de test et d'exemples

## Technologies utilisées

- **FastAPI** : API backend
- **Streamlit** : Interface utilisateur
- **Requests** : Communication HTTP
- **Pandas** : Manipulation des données
- **Scikit-learn** : Machine Learning
- **Joblib** : Sérialisation des modèles
- **Uvicorn** : Serveur ASGI pour FastAPI

## Notes

L'application Streamlit communique avec l'API FastAPI via des requêtes HTTP. Assurez-vous que l'API est démarrée avant d'utiliser l'interface Streamlit.
