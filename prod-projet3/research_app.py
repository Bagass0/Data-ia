import streamlit as st
import time
from research_agent import IntelligentResearchAgent

# Configuration de la page
st.set_page_config(
    page_title="🔍 Agent de Recherche Intelligent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    /* Variables CSS pour cohérence */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #28a745;
        --bg-light: #f8fafc;
        --bg-dark: #1e293b;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e2e8f0;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Suppression complète de l'espace en haut de page */
    .stApp > header {
        height: 0;
        display: none;
    }
    
    .stApp {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    /* Suppression des marges et paddings du conteneur principal */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Suppression de l'espace autour du contenu principal */
    .main .block-container {
        padding-top: 1rem !important;
        max-width: 100%;
    }

    /* Header principal avec gradient moderne - collé au haut */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 1rem;
        margin-top: 0;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Container de recherche avec style Glass Morphism - collé au header */
    .search-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 24px;
        margin: -0.5rem 0 2rem 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: var(--shadow-lg);
        position: relative;
    }
    
    .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 24px;
        pointer-events: none;
    }
    
    /* Cards pour résultats avec hover effect */
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border-left: 4px solid var(--primary-color);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    }
    
    /* Source cards modernisées */
    .source-card {
        background: var(--bg-light);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        transition: all 0.2s ease;
    }
    
    .source-card:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow);
    }

    /* Sidebar moderne avec design épuré */
    .sidebar .sidebar-content {
        padding-top: 1rem;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Réduction des espaces avec animation */
    .element-container {
        margin-bottom: 0.5rem !important;
        transition: all 0.2s ease;
    }
    
    /* Métriques avec style moderne */
    .sidebar .metric-container {
        padding: 0.1rem 0 !important;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 8px;
        margin: 0.2rem 0;
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .sidebar .metric-container:hover {
        background: rgba(255, 255, 255, 0.9);
        transform: scale(1.02);
    }
    
    .sidebar .metric-container > div {
        font-size: 0.6rem !important;
        font-weight: 600;
    }
    
    .sidebar .metric-container [data-testid="metric-container"] {
        font-size: 0.6rem !important;
    }
    
    .sidebar .metric-container .metric-label {
        font-size: 0.5rem !important;
        color: var(--text-secondary);
    }
    
    .sidebar .metric-container .metric-value {
        font-size: 0.6rem !important;
        line-height: 1.1 !important;
        color: var(--text-primary);
        font-weight: 700;
    }
    
    .sidebar [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 0.6rem !important;
        color: var(--primary-color);
    }
    
    .sidebar [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        font-size: 0.5rem !important;
    }
    
    /* Layout moderne - suppression du padding top pour éliminer l'espace blanc */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    /* Suppression des marges par défaut de Streamlit */
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    
    /* Suppression de l'espace au-dessus du header */
    .main {
        padding-top: 0rem !important;
    }
    
    /* Sidebar avec typographie moderne */
    .sidebar .markdown-text-container {
        font-size: 0.85rem;
        line-height: 1.5;
        color: var(--text-primary);
    }
    
    /* Titres de section avec style moderne */
    .sidebar h2, .sidebar h3 {
        color: var(--text-primary);
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 0.5rem;
    }
    
    /* Outils en vert avec badge style */
    .tool-name {
        color: var(--accent-color) !important;
        font-weight: 700;
        background: rgba(40, 167, 69, 0.1);
        padding: 2px 6px;
        border-radius: 6px;
        font-size: 0.9em;
        border: 1px solid rgba(40, 167, 69, 0.2);
    }
    
    /* Boutons avec style moderne */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Input fields modernisés */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid var(--border-color);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Progress bar moderne */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 10px;
    }
    
    /* Expander avec style moderne */
    .streamlit-expanderHeader {
        background: var(--bg-light);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-card, .source-card, .search-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .search-container {
            padding: 1.5rem;
            border-radius: 16px;
        }
        
        .result-card {
            padding: 1.5rem;
        }
    }
    
    /* Status indicators */
    .status-success {
        color: var(--accent-color);
        font-weight: 600;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: 600;
    }
    
    /* Footer moderne */
    .footer-text {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.9rem;
        padding: 2rem 0;
        border-top: 1px solid var(--border-color);
        background: var(--bg-light);
        margin-top: 3rem;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de l'agent
@st.cache_resource
def get_research_agent():
    return IntelligentResearchAgent()

agent = get_research_agent()

# =============================================================================
# BARRE LATÉRALE - Informations sur l'agent
# =============================================================================
with st.sidebar:
    st.markdown("## 🤖 Agent de Recherche")
    
    # Informations générales
    st.markdown("### 📊 Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🧠", "Mistral", delta=None)
        st.metric("🔍", "DDG", delta=None)
    with col2:
        st.metric("🌐", "BS4+Req", delta=None)
        st.metric("📈", "2.0", delta=None)
    
    # Statistiques de session
    st.markdown("### 📈 Session actuelle")
    if 'search_count' not in st.session_state:
        st.session_state.search_count = 0
    if 'total_sites_scraped' not in st.session_state:
        st.session_state.total_sites_scraped = 0
    if 'last_search_time' not in st.session_state:
        st.session_state.last_search_time = "Aucune"
    
    st.metric("🔢 Recherches", st.session_state.search_count)
    st.metric("🌐 Sites scrapés", st.session_state.total_sites_scraped)
    st.markdown(f"**⏰ Dernière recherche:** {st.session_state.last_search_time}")
    
    # Informations techniques
    st.markdown("### ⚙️ Capacités")
    st.markdown("""
    **🧠 LLM Mistral:**
    - Modèle: `mistral-small-latest`
    - Plans intelligents
    - Synthèse auto
    
    **🔍 Recherche:**
    - Moteur DuckDuckGo
    - Filtrage intelligent
    - Multi-requêtes
    
    **📖 Scraping:**
    - <span class="tool-name">BeautifulSoup4</span> + <span class="tool-name">Requests</span>
    - Extraction HTML/CSS
    - Nettoyage auto
    - Headers simulés
    
    **🎯 Types:**
    - Comparaisons
    - Prix
    - Tutoriels
    - Actualités
    - Général
    """, unsafe_allow_html=True)
    
    # État de la dernière recherche
    if 'last_research_results' in st.session_state:
        st.markdown("### 📊 Dernière recherche")
        results = st.session_state.last_research_results
        
        st.markdown(f"**🎯** {results.get('query', 'N/A')[:30]}...")
        st.markdown(f"**🧠** {results.get('intent', 'N/A')}")
        st.markdown(f"**📈** {results.get('confidence', 0):.0%} | **🌐** {results.get('sites_count', 0)} | **✅** {results.get('scraped_count', 0)}")
    
    st.markdown("---")
    st.markdown("**🔗 API:** ✅ **🌐 Web:** ✅")
    
    # Bouton pour réinitialiser les statistiques
    if st.button("🔄 Reset", use_container_width=True, type="secondary"):
        st.session_state.search_count = 0
        st.session_state.total_sites_scraped = 0
        st.session_state.last_search_time = "Aucune"
        if 'last_research_results' in st.session_state:
            del st.session_state.last_research_results
        st.rerun()

# =============================================================================
# CONTENU PRINCIPAL
# =============================================================================

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
            st.markdown("### 🔄 Recherche en cours...")
            progress_bar = st.progress(0)
        
        # Étape 1: Génération du plan LLM
        with status_placeholder.container():
            st.info("🧠 Génération du plan de recherche avec LLM...")
        
        # Mise à jour barre latérale
        sidebar_progress = st.sidebar.empty()
        with sidebar_progress.container():
            st.markdown("### 🔄 Recherche en cours")
            st.markdown("**Étape 1/5:** Génération du plan LLM...")
            st.progress(0.2)
        
        progress_bar.progress(20)
        time.sleep(1)
        
        # Étape 2: Recherche web
        with status_placeholder.container():
            st.info("🌐 Recherche sur le web...")
        
        with sidebar_progress.container():
            st.markdown("### 🔄 Recherche en cours")
            st.markdown("**Étape 2/5:** Recherche web...")
            st.progress(0.4)
        
        progress_bar.progress(40)
        time.sleep(1)
        
        # Étape 3: Filtrage des sites
        with status_placeholder.container():
            st.info("🎯 Filtrage des sites pertinents...")
        
        with sidebar_progress.container():
            st.markdown("### 🔄 Recherche en cours")
            st.markdown("**Étape 3/5:** Filtrage des sites...")
            st.progress(0.6)
        
        progress_bar.progress(60)
        time.sleep(1)
        
        # Étape 4: Scraping
        with status_placeholder.container():
            st.info("📖 Extraction du contenu des sites...")
        
        with sidebar_progress.container():
            st.markdown("### 🔄 Recherche en cours")
            st.markdown("**Étape 4/5:** Scraping des sites...")
            st.progress(0.8)
        
        progress_bar.progress(80)
        
        # Exécution de la recherche complète
        try:
            results = agent.full_research(query)
            
            # Mise à jour des statistiques de session
            st.session_state.search_count += 1
            st.session_state.total_sites_scraped += len(results["scraped_contents"])
            st.session_state.last_search_time = time.strftime("%H:%M:%S")
            
            # Sauvegarde des résultats pour la barre latérale
            synthesis = results["synthesis"]
            plan = results["research_plan"]
            st.session_state.last_research_results = {
                'query': query,
                'intent': plan["analysis"]["intent"].replace("_", " ").title(),
                'confidence': synthesis['confidence'],
                'sites_count': len(results["search_results"]),
                'scraped_count': len(results["scraped_contents"])
            }
            
            with status_placeholder.container():
                st.info("🤖 Synthèse intelligente avec LLM...")
            
            with sidebar_progress.container():
                st.markdown("### 🔄 Recherche en cours")
                st.markdown("**Étape 5/5:** Synthèse avec LLM...")
                st.progress(1.0)
            
            progress_bar.progress(100)
            time.sleep(0.5)
            
            # Nettoyage des indicateurs
            progress_placeholder.empty()
            status_placeholder.empty()
            sidebar_progress.empty()
            
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
                st.markdown("#### 💡 Recommandations:")
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
<div class="footer-text">
    🔍 <strong>Agent de Recherche Intelligent</strong> - Propulsé par <span class="tool-name">Mistral AI</span> + <span class="tool-name">Web Scraping</span>
    <br><small>Interface moderne • Recherche intelligente • Synthèse automatisée</small>
</div>
""", unsafe_allow_html=True)
