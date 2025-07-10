import streamlit as st
import requests
import pandas as pd

# Configuration de l'API
API_BASE_URL = "http://127.0.0.1:8000"

def check_api_status():
    """Vérifie si l'API est accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def predict_via_api(size: float, nb_rooms: int, garden: int):
    """Fait une prédiction via l'API"""
    try:
        payload = {
            "size": size,
            "nb_rooms": nb_rooms,
            "garden": garden
        }
        response = requests.post(f"{API_BASE_URL}/predict", json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur API: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API: {e}")
        return None

# Interface Streamlit
st.title("Prédiction du prix d'une maison via API")
st.write("Entrez les caractéristiques de la maison pour prédire son prix")

# Vérification du statut de l'API
api_status = check_api_status()
if api_status:
    st.success("✅ API connectée et fonctionnelle")
else:
    st.error("❌ API non accessible. Assurez-vous que le serveur FastAPI est démarré sur http://127.0.0.1:8000")
    st.info("💡 Pour démarrer l'API, exécutez: `uvicorn main:app --reload` dans le dossier backend")
    st.stop()

# Création des champs de formulaire
st.subheader("Caractéristiques de la maison")

# Champ pour la taille
size = st.number_input(
    "Taille de la maison (en m²)", 
    min_value=0.0, 
    max_value=1000.0, 
    value=100.0,
    step=1.0
)

# Champ pour le nombre de chambres
nb_rooms = st.number_input(
    "Nombre de chambres", 
    min_value=0, 
    max_value=20, 
    value=3,
    step=1
)

# Champ pour le jardin (0 = non, 1 = oui)
garden = st.number_input(
    "Jardin (0 = Non, 1 = Oui)", 
    min_value=0, 
    max_value=1, 
    value=0,
    step=1
)

# Bouton de prédiction
if st.button("Prédire le prix"):
    # Validation des données
    if size <= 0:
        st.error("La taille doit être supérieure à 0")
    elif nb_rooms < 0:
        st.error("Le nombre de chambres ne peut pas être négatif")
    else:
        # Affichage d'un spinner pendant la prédiction
        with st.spinner("Prédiction en cours..."):
            # Appel à l'API
            result = predict_via_api(size, nb_rooms, garden)
            
            if result:
                predicted_price = result["predicted_price"]
                
                # Affichage du résultat
                st.success(f"Prix prédit de la maison : {predicted_price:,.2f} €")
                
                # Affichage des détails
                st.write("---")
                st.write("**Détails de la prédiction :**")
                st.write(f"- Taille : {size} m²")
                st.write(f"- Nombre de chambres : {int(nb_rooms)}")
                st.write(f"- Jardin : {'Oui' if garden == 1 else 'Non'}")
                st.write(f"- **Prix prédit : {predicted_price:,.2f} €**")
                
                # Informations techniques
                with st.expander("ℹ️ Informations techniques"):
                    st.json(result)
            else:
                st.error("Impossible d'obtenir une prédiction. Vérifiez que l'API fonctionne correctement.")

# Section d'informations sur l'API
st.write("---")
st.subheader("🔗 Informations sur l'API")
col1, col2 = st.columns(2)

with col1:
    if st.button("Tester la connexion API"):
        if check_api_status():
            st.success("API accessible ✅")
        else:
            st.error("API non accessible ❌")

with col2:
    if st.button("Voir exemples de prédictions"):
        try:
            response = requests.get(f"{API_BASE_URL}/predictions/samples", timeout=5)
            if response.status_code == 200:
                examples = response.json()
                st.subheader("Exemples de prédictions depuis l'API:")
                for i, example in enumerate(examples, 1):
                    st.write(f"**Exemple {i}:**")
                    st.write(f"- Taille: {example['size']} m²")
                    st.write(f"- Chambres: {example['nb_rooms']}")
                    st.write(f"- Jardin: {'Oui' if example['garden'] == 1 else 'Non'}")
                    st.write(f"- Prix prédit: {example['predicted_price']:,.2f} €")
                    st.write("---")
            else:
                st.error("Erreur lors de la récupération des exemples")
        except requests.exceptions.RequestException:
            st.error("Impossible de récupérer les exemples depuis l'API")
