import streamlit as st
import time
from research_agent import IntelligentResearchAgent

# Configuration de la page
st.set_page_config(
    page_title="🔍 Agent de Recherche Intelligent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .search-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .source-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'agent
@st.cache_resource
def get_research_agent():
    return IntelligentResearchAgent()

agent = get_research_agent()

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🔍 Agent de Recherche Intelligent</h1>
    <p>Recherche intelligente avec plan LLM et scraping réel</p>
</div>
""", unsafe_allow_html=True)

# Interface de recherche
st.markdown('<div class="search-container">', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "",
        placeholder="Ex: meilleurs casques moto 2025, prix immobilier Paris, comment apprendre Python...",
        help="Posez votre question - l'agent créera un plan et cherchera sur les sites pertinents",
        label_visibility="collapsed"
    )

with col2:
    search_button = st.button("🚀 Rechercher", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Exemples de recherches
with st.expander("💡 Exemples de recherches"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏍️ Meilleurs casques moto", use_container_width=True):
            st.experimental_set_query_params(q="meilleurs casques moto 2025")
        if st.button("🏠 Prix immobilier Paris", use_container_width=True):
            st.experimental_set_query_params(q="prix immobilier Paris 2025")
    
    with col2:
        if st.button("💻 Apprendre Python", use_container_width=True):
            st.experimental_set_query_params(q="comment apprendre Python débutant")
        if st.button("📱 Meilleurs smartphones", use_container_width=True):
            st.experimental_set_query_params(q="meilleurs smartphones 2025 comparatif")

# Traitement de la recherche
if search_button and query:
    
    # Conteneur pour les résultats
    results_container = st.container()
    
    with results_container:
        # Indicateur de progression
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        with progress_placeholder.container():
            st.markdown("### � Recherche en cours...")
            progress_bar = st.progress(0)
        
        # Étape 1: Génération du plan LLM
        with status_placeholder.container():
            st.info("🧠 Génération du plan de recherche avec LLM...")
        progress_bar.progress(20)
        time.sleep(1)
        
        # Étape 2: Recherche web
        with status_placeholder.container():
            st.info("🌐 Recherche sur le web...")
        progress_bar.progress(40)
        time.sleep(1)
        
        # Étape 3: Filtrage des sites
        with status_placeholder.container():
            st.info("� Filtrage des sites pertinents...")
        progress_bar.progress(60)
        time.sleep(1)
        
        # Étape 4: Scraping
        with status_placeholder.container():
            st.info("📖 Extraction du contenu des sites...")
        progress_bar.progress(80)
        
        # Exécution de la recherche complète
        try:
            results = agent.full_research(query)
            
            with status_placeholder.container():
                st.info("🤖 Synthèse intelligente avec LLM...")
            progress_bar.progress(100)
            time.sleep(0.5)
            
            # Nettoyage des indicateurs
            progress_placeholder.empty()
            status_placeholder.empty()
            
            # Affichage des résultats
            st.markdown("---")
            st.markdown("## 📊 Résultats de la recherche")
            
            # Métriques
            synthesis = results["synthesis"]
            plan = results["research_plan"]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Sites scrapés", len(results["scraped_contents"]))
            with col2:
                st.metric("📊 Confiance", f"{synthesis['confidence']:.0%}")
            with col3:
                st.metric("🧠 Type détecté", plan["analysis"]["intent"].replace("_", " ").title())
            with col4:
                st.metric("📈 Sources", len(results["search_results"]))
            
            # Plan de recherche LLM
            with st.expander("🧠 Plan généré par LLM", expanded=True):
                st.markdown("**Intention détectée:** " + plan["analysis"]["intent"].replace("_", " ").title())
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Sites cibles:**")
                    for site in plan["target_sites"]:
                        st.markdown(f"- {site['name']} ({site['search_type']})")
                
                with col2:
                    st.markdown("**Stratégies de recherche:**")
                    for strategy in plan["search_strategy"]:
                        st.markdown(f"- {strategy}")
            
            # Synthèse principale
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown("### 📝 Synthèse intelligente")
            st.markdown(synthesis["summary"])
            
            if synthesis["key_points"]:
                st.markdown("#### 🔑 Points clés:")
                for point in synthesis["key_points"]:
                    st.markdown(f"• {point}")
            
            if synthesis["recommendations"]:
                st.markdown("#### � Recommandations:")
                for rec in synthesis["recommendations"]:
                    st.markdown(f"• {rec}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Sources scrapées
            st.markdown("### 📚 Sites analysés")
            
            for i, content in enumerate(results["scraped_contents"], 1):
                search_result = content.get("search_result", {})
                
                with st.expander(f"📄 Source {i}: {content['title'][:50]}..." if len(content['title']) > 50 else f"📄 Source {i}: {content['title']}"):
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**URL:** {content['url']}")
                        st.markdown(f"**Statut:** {'✅ Succès' if content['status'] == 'success' else '❌ Erreur'}")
                        if content['status'] == 'success':
                            st.markdown(f"**Mots:** {content['word_count']}")
                    
                    with col2:
                        domain = content['url'].split('/')[2] if '/' in content['url'] else content['url']
                        st.markdown(f"**Domaine:** {domain}")
                        if search_result.get('relevance_score'):
                            st.markdown(f"**Pertinence:** {search_result['relevance_score']:.1%}")
                    
                    if content['status'] == 'success' and content['content']:
                        st.markdown("**Extrait du contenu:**")
                        preview = content['content'][:500] + "..." if len(content['content']) > 500 else content['content']
                        st.text_area("", preview, height=100, disabled=True, key=f"content_{i}")
                    else:
                        st.warning(f"Contenu non accessible: {content['content']}")
            
            # Données techniques (optionnel)
            with st.expander("🔬 Données techniques"):
                tab1, tab2 = st.tabs(["Plan LLM", "Résultats bruts"])
                
                with tab1:
                    st.json(results["research_plan"])
                
                with tab2:
                    st.json(results["search_results"])
                    
        except Exception as e:
            progress_placeholder.empty()
            status_placeholder.empty()
            st.error(f"❌ Erreur lors de la recherche: {str(e)}")
            st.info("💡 Vérifiez votre connexion internet et réessayez")

# Section informative si pas de recherche
elif not query:
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Comment ça marche ?")
        st.markdown("""
        1. **🧠 Plan LLM** - L'agent analyse votre requête et crée un plan intelligent
        2. **🌐 Recherche web** - Recherche sur les moteurs avec DuckDuckGo  
        3. **🎯 Filtrage** - Sélectionne les sites pertinents selon le plan
        4. **📖 Scraping** - Extrait le contenu réel des sites web
        5. **🤖 Synthèse** - Analyse et résume avec intelligence artificielle
        """)
    
    with col2:
        st.markdown("### 🚀 Types de recherches supportées")
        st.markdown("""
        - **🛍️ Comparaisons produits** - "meilleurs casques moto"
        - **💰 Recherches prix** - "prix immobilier Paris" 
        - **📚 Tutoriels** - "comment apprendre Python"
        - **📰 Actualités** - "nouveautés IA 2025"
        - **🔍 Recherches générales** - tout autre sujet
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    🔍 Agent de Recherche Intelligent - LLM + Scraping Réel
</div>
""", unsafe_allow_html=True)
