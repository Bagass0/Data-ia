import streamlit as st
import joblib
import pandas as pd

# Chargement du modèle
@st.cache_resource
def load_model():
    model = joblib.load("assets/regression.joblib")
    return model

# Interface Streamlit
st.title("Prédiction du prix d'une maison")
st.write("Entrez les caractéristiques de la maison pour prédire son prix")

# Chargement du modèle
model = load_model()

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
    # Préparation des données pour la prédiction
    input_data = pd.DataFrame({
        'size': [size],
        'nb_rooms': [nb_rooms],
        'garden': [garden]
    })
    
    # Prédiction
    prediction = model.predict(input_data)
    
    # Affichage du résultat
    st.success(f"Prix prédit de la maison : {prediction[0]:,.2f} €")
    
    # Affichage des détails
    st.write("---")
    st.write("**Détails de la prédiction :**")
    st.write(f"- Taille : {size} m²")
    st.write(f"- Nombre de chambres : {int(nb_rooms)}")
    st.write(f"- Jardin : {'Oui' if garden == 1 else 'Non'}")
    st.write(f"- **Prix prédit : {prediction[0]:,.2f} €**")
