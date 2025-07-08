import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="🎮 Jeux Vidéo Dashboard", 
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-weight: 700;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stTabs > div > div > div > div {
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .stMultiSelect > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .stSlider > div > div > div > div {
        background-color: #667eea;
    }
    
    .footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 3rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #2196f3;
    }
    
    .insight-box h4 {
        color: #1976d2 !important;
        margin-top: 0;
    }
    
    .insight-box p {
        color: #424242 !important;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #ff9800;
    }
    
    .warning-box h4 {
        color: #f57c00 !important;
        margin-top: 0;
    }
    
    .warning-box p, .warning-box ul, .warning-box li {
        color: #424242 !important;
    }
    
    /* Améliorer la lisibilité du texte */
    .stMarkdown p {
        color: #424242 !important;
    }
    
    /* Titres des sections */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #1976d2 !important;
    }
    
    /* Sidebar améliorée */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Améliorer les métriques */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stMetric .metric-value {
        color: #667eea !important;
    }
    
    .stMetric .metric-label {
        color: #6c757d !important;
    }
</style>
""", unsafe_allow_html=True)

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")
    # Renommer la colonne pour plus de clarté
    df.rename(columns={"Year_of_Release": "Year"}, inplace=True)
    # Supprimer les lignes avec des valeurs manquantes dans les colonnes essentielles
    df.dropna(subset=["Year", "Genre", "Platform", "Global_Sales"], inplace=True)
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()

# Sidebar améliorée avec navigation
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 1rem;'><h2 style='color: #667eea; margin: 0;'>🎮 Gaming Analytics</h2></div>", unsafe_allow_html=True)
    
    # Navigation menu
    selected = option_menu(
        menu_title=None,
        options=["📊 Dashboard", "🎯 Analyse", "📈 Tendances"],
        icons=["bar-chart", "bullseye", "graph-up"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#667eea", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e3f2fd"},
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )
    
    st.markdown("---")
    
    # Filtres
    st.markdown("### 🔍 Filtres")
    year_range = st.slider("Année de sortie", int(df["Year"].min()), int(df["Year"].max()), (2000, 2015))
    selected_platforms = st.multiselect("Plateforme(s)", options=sorted(df["Platform"].unique()), default=["PS2", "X360", "PC"])
    selected_genres = st.multiselect("Genre(s)", options=sorted(df["Genre"].unique()), default=["Action", "Shooter", "Sports"])
    
    # Statistiques rapides
    st.markdown("---")
    st.markdown("### 📊 Statistiques rapides")
    total_games = len(df)
    total_sales = df["Global_Sales"].sum()
    avg_score = df["Critic_Score"].mean() if "Critic_Score" in df.columns else 0
    
    st.metric("Total Jeux", f"{total_games:,}")
    st.metric("Ventes Totales", f"{total_sales:.1f}M")
    if avg_score > 0:
        st.metric("Score Moyen", f"{avg_score:.1f}/100")

# Filtrage
df_filtered = df[
    (df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1]) &
    (df["Platform"].isin(selected_platforms)) &
    (df["Genre"].isin(selected_genres))
]

# Titre principal avec design amélioré
st.markdown('<div class="main-header"><h1>🎮 Gaming Analytics Dashboard</h1></div>', unsafe_allow_html=True)

# Métriques principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(df_filtered):,}</div>
        <div class="metric-label">Jeux analysés</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_sales_filtered = df_filtered["Global_Sales"].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_sales_filtered:.1f}M</div>
        <div class="metric-label">Ventes totales</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_sales = df_filtered["Global_Sales"].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_sales:.2f}M</div>
        <div class="metric-label">Ventes moyennes</div>
    </div>
    """, unsafe_allow_html=True)
    # Ajout intervalle de confiance avec numpy
    sales = df_filtered["Global_Sales"].dropna()
    mean_sales = np.mean(sales)
    std_sales = np.std(sales)
    n = len(sales)
    conf_interval = 1.96 * std_sales / np.sqrt(n)  # 95% confidence
    st.markdown(f"<div style='font-size:0.9rem;color:#1976d2;'>IC 95% : ±{conf_interval:.2f}M</div>", unsafe_allow_html=True)

with col4:
    top_genre = df_filtered.groupby("Genre")["Global_Sales"].sum().idxmax()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{top_genre}</div>
        <div class="metric-label">Genre dominant</div>
    </div>
    """, unsafe_allow_html=True)

# Insight box
st.markdown(f"""
<div class="insight-box">
    <h4 style="color: #1976d2;">📈 Insights clés</h4>
    <p style="color: #424242;">Analyse de <strong>{len(df_filtered)} jeux</strong> entre <strong>{year_range[0]}</strong> et <strong>{year_range[1]}</strong></p>
    <p style="color: #424242;">• Période couverte : {year_range[1] - year_range[0]} années</p>
    <p style="color: #424242;">• Plateformes sélectionnées : {', '.join(selected_platforms)}</p>
    <p style="color: #424242;">• Genres analysés : {', '.join(selected_genres)}</p>
</div>
""", unsafe_allow_html=True)

# Navigation entre les pages
if selected == "📊 Dashboard":
    # Contenu du Dashboard principal
    
    # --- Ventes mondiales par genre ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💡 Ventes globales par genre")
    genre_sales = df_filtered.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)

    fig1 = px.bar(
        x=genre_sales.values,
        y=genre_sales.index,
        orientation='h',
        title="Ventes par genre (en millions)",
        color=genre_sales.values,
        color_continuous_scale="viridis",
        labels={'x': 'Ventes (millions)', 'y': 'Genre'}
    )
    fig1.update_layout(
        height=500,
        showlegend=False,
        title_font_size=16,
        font=dict(size=12, color='#424242'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Top 10 jeux ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🏆 Top 10 jeux par ventes globales")
    top_games = df_filtered.sort_values(by="Global_Sales", ascending=False).head(10)

    fig2 = px.bar(
        top_games,
        x="Global_Sales",
        y="Name",
        orientation='h',
        title="Top 10 des jeux les plus vendus",
        color="Global_Sales",
        color_continuous_scale="plasma",
        labels={'Global_Sales': 'Ventes (millions)', 'Name': 'Jeu'}
    )
    fig2.update_layout(
        height=500,
        showlegend=False,
        title_font_size=16,
        font=dict(size=12, color='#424242'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Ventes par année ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Ventes totales par année")
    sales_by_year = df_filtered.groupby("Year")["Global_Sales"].sum().reset_index()

    fig3 = px.line(
        sales_by_year,
        x="Year",
        y="Global_Sales",
        title="Évolution des ventes par année",
        markers=True,
        line_shape="spline"
    )
    fig3.update_traces(
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#764ba2')
    )
    fig3.update_layout(
        height=400,
        title_font_size=16,
        font=dict(size=12, color='#424242'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Année",
        yaxis_title="Ventes (millions)"
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "🎯 Analyse":
    # Page d'analyse détaillée
    st.markdown('<div class="main-header"><h1>🎯 Analyse Détaillée</h1></div>', unsafe_allow_html=True)
    
    # --- Analyses par plateforme ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎮 Répartition des ventes par plateforme")
    platform_sales = df_filtered.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(10)

    fig4 = px.pie(
        values=platform_sales.values,
        names=platform_sales.index,
        title="Top 10 plateformes par ventes",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig4.update_layout(
        height=500,
        title_font_size=16,
        font=dict(size=12, color='#424242'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Heatmap des ventes par genre et plateforme ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🔥 Heatmap Genre vs Plateforme (Plotly)")
    # Créer une matrice de corrélation
    heatmap_data = df_filtered.groupby(["Genre", "Platform"])["Global_Sales"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="Genre", columns="Platform", values="Global_Sales").fillna(0)
    # Sélectionner les top plateformes pour éviter un graphique trop chargé
    top_platforms = df_filtered.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(8).index
    heatmap_pivot = heatmap_pivot[top_platforms]
    fig5 = px.imshow(
        heatmap_pivot,
        aspect="auto",
        color_continuous_scale="Viridis",
        title="Ventes par Genre et Plateforme (Top 8 plateformes)"
    )
    fig5.update_layout(
        height=500,
        title_font_size=16,
        font=dict(size=12, color='#424242'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # Ajout heatmap matplotlib/seaborn
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🔥 Heatmap Genre vs Plateforme (Seaborn/Matplotlib)")
    top5_platforms = df_filtered.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(5).index
    heatmap_data2 = df_filtered[df_filtered["Platform"].isin(list(top5_platforms))]
    pivot2 = heatmap_data2.pivot_table(index="Genre", columns="Platform", values="Global_Sales", aggfunc="sum", fill_value=0)
    fig_sea, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot2, annot=True, fmt=".1f", cmap="Blues", ax=ax)
    st.pyplot(fig_sea)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Note critique vs ventes (si dispo) ---
    if "Critic_Score" in df.columns:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🎯 Corrélation : Note critique vs Ventes")
        df_score = df_filtered.dropna(subset=["Critic_Score"])
        
        fig6 = px.scatter(
            df_score, 
            x="Critic_Score", 
            y="Global_Sales",
            color="Genre",
            size="Global_Sales",
            hover_data=["Name", "Platform", "Year"],
            title="Relation entre note critique et ventes",
            labels={'Critic_Score': 'Note Critique', 'Global_Sales': 'Ventes (millions)'}
        )
        fig6.update_layout(
            height=500,
            title_font_size=16,
            font=dict(size=12, color='#424242'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Section d'analyse comparative ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🔍 Analyse comparative des éditeurs")
    col1, col2 = st.columns(2)

    with col1:
        # Top éditeurs
        if "Publisher" in df.columns:
            top_publishers = df_filtered.groupby("Publisher")["Global_Sales"].sum().sort_values(ascending=False).head(10)
            fig8 = px.bar(
                x=top_publishers.index,
                y=top_publishers.values,
                title="Top 10 éditeurs par ventes",
                color=top_publishers.values,
                color_continuous_scale="Blues"
            )
            fig8.update_layout(
                height=400,
                xaxis_tickangle=-45,
                showlegend=False,
                title_font_size=14,
                font=dict(size=10, color='#424242'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig8, use_container_width=True)

    with col2:
        # Répartition des ventes par région
        if all(col in df.columns for col in ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]):
            region_sales = {
                "Amérique du Nord": df_filtered["NA_Sales"].sum(),
                "Europe": df_filtered["EU_Sales"].sum(),
                "Japon": df_filtered["JP_Sales"].sum(),
                "Autres": df_filtered["Other_Sales"].sum()
            }
            fig9 = px.pie(
                values=list(region_sales.values()),
                names=list(region_sales.keys()),
                title="Répartition des ventes par région",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig9.update_layout(
                height=400,
                title_font_size=14,
                font=dict(size=10, color='#424242'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig9, use_container_width=True)
            # Ajout donut chart plotly.graph_objects
            fig_go = go.Figure(data=[go.Pie(labels=list(region_sales.keys()), values=list(region_sales.values()), hole=.4)])
            fig_go.update_layout(title_text="Répartition des ventes par région (Plotly GO)")
            st.plotly_chart(fig_go, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "📈 Tendances":
    # Page des tendances
    st.markdown('<div class="main-header"><h1>📈 Tendances & Évolutions</h1></div>', unsafe_allow_html=True)
    
    # --- Analyses temporelles avancées ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Évolution des genres dans le temps")
    # Analyse de l'évolution des genres par année
    genre_year = df_filtered.groupby(["Year", "Genre"])["Global_Sales"].sum().reset_index()
    top_genres = df_filtered.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).head(6).index
    genre_year_filtered = genre_year[genre_year["Genre"].isin(list(top_genres))]

    fig7 = px.line(
        genre_year_filtered,
        x="Year",
        y="Global_Sales",
        color="Genre",
        title="Évolution des ventes par genre (Top 6 genres)",
        markers=True
    )
    fig7.update_layout(
        height=500,
        title_font_size=16,
        font=dict(size=12, color='#424242'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Année",
        yaxis_title="Ventes (millions)"
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Analyse des cycles de plateformes ---
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🎮 Cycles de vie des plateformes")
    platform_year = df_filtered.groupby(["Year", "Platform"])["Global_Sales"].sum().reset_index()
    top_platforms_trend = df_filtered.groupby("Platform")["Global_Sales"].sum().sort_values(ascending=False).head(8).index
    platform_year_filtered = platform_year[platform_year["Platform"].isin(list(top_platforms_trend))]

    fig_platform = px.line(
        platform_year_filtered,
        x="Year",
        y="Global_Sales",
        color="Platform",
        title="Évolution des ventes par plateforme (Top 8 plateformes)",
        markers=True
    )
    fig_platform.update_layout(
        height=500,
        title_font_size=16,
        font=dict(size=12, color='#424242'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Année",
        yaxis_title="Ventes (millions)"
    )
    st.plotly_chart(fig_platform, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Analyse des scores utilisateurs vs critiques ---
    if "User_Score" in df.columns and "Critic_Score" in df.columns:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("👥 Scores Utilisateurs vs Critiques")
        df_both_scores = df_filtered.dropna(subset=["User_Score", "Critic_Score"])
        
        # Convertir User_Score en numérique si nécessaire
        df_both_scores = df_both_scores.copy()
        df_both_scores["User_Score"] = pd.to_numeric(df_both_scores["User_Score"], errors='coerce')
        df_both_scores = df_both_scores.dropna(subset=["User_Score"])
        df_both_scores["User_Score"] = df_both_scores["User_Score"] * 10  # Convertir en échelle 0-100

        fig_scores = px.scatter(
            df_both_scores, 
            x="Critic_Score", 
            y="User_Score",
            color="Genre",
            size="Global_Sales",
            hover_data=["Name", "Platform", "Year"],
            title="Corrélation entre scores critiques et utilisateurs",
            labels={'Critic_Score': 'Score Critique', 'User_Score': 'Score Utilisateur'}
        )
        fig_scores.update_layout(
            height=500,
            title_font_size=16,
            font=dict(size=12, color='#424242'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_scores, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Prédictions et insights ---
    st.markdown("""
    <div class="warning-box">
        <h4 style="color: #f57c00;">📊 Analyse des tendances</h4>
        <p style="color: #424242;"><strong>Observations clés :</strong></p>
        <ul style="color: #424242;">
            <li><strong>Pic de l'industrie</strong> : Les années 2008-2009 marquent l'apogée des ventes</li>
            <li><strong>Évolution des genres</strong> : Déclin des jeux de sport, montée du Action</li>
            <li><strong>Cycles de plateformes</strong> : Durée de vie moyenne de 6-8 ans par génération</li>
            <li><strong>Corrélation qualité-ventes</strong> : Relation positive mais non linéaire</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- Recommandations et insights ---
st.markdown("""
<div class="warning-box">
    <h4 style="color: #f57c00;">🎯 Recommandations stratégiques</h4>
    <ul style="color: #424242;">
        <li><strong>Genres porteurs</strong> : Concentrez-vous sur les genres Action, Sports et Shooter qui dominent les ventes</li>
        <li><strong>Plateformes clés</strong> : PS2, X360 et Wii représentent les plateformes les plus lucratives</li>
        <li><strong>Timing</strong> : La période 2005-2010 montre les pics de ventes les plus élevés</li>
        <li><strong>Marché global</strong> : L'Amérique du Nord reste le marché dominant, suivi de l'Europe</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer amélioré
st.markdown("""
<div class="footer">
    <h3>🎮 Gaming Analytics Dashboard</h3>
    <p>Analyse complète des données de ventes de jeux vidéo (1980-2016)</p>
    <p>💡 <strong>Insights</strong> • 📊 <strong>Visualisations interactives</strong> • 🎯 <strong>Recommandations</strong></p>
    <hr style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.3);">
    <p style="margin: 0; font-size: 0.9rem;">
        👨‍💻 Développé avec <strong>Streamlit</strong> & <strong>Plotly</strong> | 
        📊 Dataset : <a href="https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings" 
        style="color: #bbdefb; text-decoration: none;">Kaggle - Video Game Sales</a>
    </p>
</div>
""", unsafe_allow_html=True)
