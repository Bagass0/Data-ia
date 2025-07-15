import streamlit as st
import requests
from research_agent import ResearchAgent

# Configuration de la page
st.set_page_config(
    page_title="Plateforme IA - Prédiction & Recherche",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar pour navigation
with st.sidebar:
    st.title("🚀 Plateforme IA")
    
    app_mode = st.selectbox(
        "Choisissez une application :",
        ["🏠 Prédiction Prix Maison", "🔍 Agent de Recherche", "📊 Tableau de Bord"]
    )
    
    st.markdown("---")
    st.markdown("### 📋 Applications disponibles")
    st.markdown("""
    - **🏠 Prédiction Prix** : Estimez le prix d'une maison
    - **🔍 Agent de Recherche** : Recherche intelligente
    - **📊 Tableau de Bord** : Vue d'ensemble
    """)

# Application Prédiction Prix Maison
if app_mode == "🏠 Prédiction Prix Maison":
    st.title("🏠 Prédiction du Prix d'une Maison")
    
    # Configuration de l'API
    API_BASE_URL = "http://127.0.0.1:8000"
    
    def check_api_status():
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def predict_via_api(size: float, nb_rooms: int, garden: int):
        try:
            payload = {"size": size, "nb_rooms": nb_rooms, "garden": garden}
            response = requests.post(f"{API_BASE_URL}/predict", json=payload, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Erreur API: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API: {e}")
            return None
    
    # Vérification du statut de l'API
    api_status = check_api_status()
    if api_status:
        st.success("✅ API connectée et fonctionnelle")
    else:
        st.error("❌ API non accessible")
        st.info("💡 Démarrez l'API avec: `uvicorn main:app --reload`")
    
    # Interface de prédiction
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Caractéristiques de la maison")
        
        size = st.number_input("Taille (m²)", min_value=0.0, max_value=1000.0, value=100.0, step=1.0)
        nb_rooms = st.number_input("Nombre de chambres", min_value=0, max_value=20, value=3, step=1)
        garden = st.selectbox("Jardin", options=[0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")
        
        predict_button = st.button("🔮 Prédire le prix", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("📊 Résultat de la prédiction")
        
        if predict_button and api_status:
            with st.spinner("Prédiction en cours..."):
                result = predict_via_api(size, nb_rooms, garden)
                
                if result:
                    price = result["predicted_price"]
                    st.success(f"💰 Prix prédit: {price:,.2f} €")
                    
                    # Détails
                    st.write("**Détails:**")
                    st.write(f"- Taille: {size} m²")
                    st.write(f"- Chambres: {int(nb_rooms)}")
                    st.write(f"- Jardin: {'Oui' if garden == 1 else 'Non'}")

# Application Agent de Recherche
elif app_mode == "🔍 Agent de Recherche":
    st.title("🔍 Agent de Recherche Intelligent")
    
    # Initialisation de l'agent
    @st.cache_resource
    def get_research_agent():
        return ResearchAgent()
    
    agent = get_research_agent()
    
    # Interface de recherche
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Que souhaitez-vous rechercher ?",
            placeholder="Ex: actualités intelligence artificielle",
            help="Posez votre question ou tapez un sujet"
        )
    
    with col2:
        search_button = st.button("🚀 Rechercher", type="primary", use_container_width=True)
    
    # Exécution de la recherche
    if search_button and query:
        with st.spinner("Agent en action..."):
            # Barre de progression
            progress = st.progress(0)
            status = st.empty()
            
            # Étapes de recherche
            status.text("📝 Analyse de la requête...")
            progress.progress(33)
            
            full_results = agent.full_research(query)
            
            status.text("🌐 Recherche en cours...")
            progress.progress(66)
            
            status.text("✅ Synthèse...")
            progress.progress(100)
            
            # Nettoyage
            progress.empty()
            status.empty()
        
        # Affichage des résultats
        synthesis = full_results["synthesis"]
        
        # Métriques
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Résultats", synthesis["total_results"])
        with col2:
            st.metric("Confiance", f"{synthesis['confidence']:.1%}")
        with col3:
            st.metric("Type", full_results["query_analysis"]["query_type"].title())
        
        # Résumé
        st.subheader("📝 Synthèse")
        st.info(synthesis["summary"])
        
        # Points clés
        if synthesis["key_points"]:
            st.subheader("🔑 Points clés")
            for i, point in enumerate(synthesis["key_points"], 1):
                st.write(f"**{i}.** {point}")
        
        # Sources
        st.subheader("📚 Sources")
        for i, source in enumerate(synthesis["sources"], 1):
            with st.expander(f"Source {i}: {source['title']}"):
                st.write(f"**Provenance:** {source['source']}")
                if source.get('url'):
                    st.write(f"**URL:** {source['url']}")

# Tableau de Bord
elif app_mode == "📊 Tableau de Bord":
    st.title("📊 Tableau de Bord - Plateforme IA")
    
    # Métriques générales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏠 Prédictions", "127", delta="12")
    
    with col2:
        st.metric("🔍 Recherches", "89", delta="23")
    
    with col3:
        st.metric("⚡ API Status", "Actif", delta="100%")
    
    with col4:
        st.metric("👥 Utilisateurs", "45", delta="7")
    
    st.markdown("---")
    
    # Statut des services
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Statut des Services")
        
        # Vérification API Prédiction
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=3)
            if response.status_code == 200:
                st.success("✅ API Prédiction - Fonctionnelle")
            else:
                st.error("❌ API Prédiction - Erreur")
        except:
            st.error("❌ API Prédiction - Non accessible")
        
        # Agent de recherche
        try:
            agent = ResearchAgent()
            st.success("✅ Agent de Recherche - Fonctionnel")
        except:
            st.error("❌ Agent de Recherche - Erreur")
    
    with col2:
        st.subheader("📈 Activité récente")
        
        st.markdown("""
        **Dernières activités:**
        - 🏠 Prédiction maison 120m² - Il y a 2 min
        - 🔍 Recherche "actualités IA" - Il y a 5 min
        - 🏠 Prédiction maison 85m² - Il y a 8 min
        - 🔍 Recherche "prix immobilier" - Il y a 12 min
        """)
    
    # Informations système
    st.markdown("---")
    st.subheader("ℹ️ Informations Système")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏠 Module Prédiction:**
        - Modèle: Régression Linéaire
        - Précision: 85%
        - Dernière mise à jour: Aujourd'hui
        """)
    
    with col2:
        st.markdown("""
        **🔍 Module Recherche:**
        - Agent: Multi-sources
        - Stratégies: 3 types
        - Synthèse: Automatique
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    🚀 Plateforme IA - Prédiction & Recherche Intelligente
</div>
""", unsafe_allow_html=True)
