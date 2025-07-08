import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Jeux Vidéo Dashboard", layout="wide")

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

# Sidebar : Filtres
st.sidebar.title("🎮 Filtres")
year_range = st.sidebar.slider("Année de sortie", int(df["Year"].min()), int(df["Year"].max()), (2000, 2015))
selected_platforms = st.sidebar.multiselect("Plateforme(s)", options=sorted(df["Platform"].unique()), default=["PS2", "X360", "PC"])
selected_genres = st.sidebar.multiselect("Genre(s)", options=sorted(df["Genre"].unique()), default=["Action", "Shooter", "Sports"])

# Filtrage
df_filtered = df[
    (df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1]) &
    (df["Platform"].isin(selected_platforms)) &
    (df["Genre"].isin(selected_genres))
]

# Titre principal
st.title("📊 Analyse des ventes de jeux vidéo (1980–2016)")

# Résumé
st.markdown(f"**{len(df_filtered)} jeux** affichés entre **{year_range[0]}** et **{year_range[1]}** sur les plateformes sélectionnées.")

# --- Ventes mondiales par genre ---
st.subheader("💡 Ventes globales par genre")
genre_sales = df_filtered.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=genre_sales.values, y=genre_sales.index, ax=ax1, palette="viridis")
ax1.set_xlabel("Ventes (en millions)")
ax1.set_ylabel("Genre")
st.pyplot(fig1)

# --- Top 10 jeux ---
st.subheader("🏆 Top 10 jeux par ventes globales")
top_games = df_filtered.sort_values("Global_Sales", ascending=False).head(10)

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_games["Global_Sales"], y=top_games["Name"], ax=ax2, palette="magma")
ax2.set_xlabel("Ventes (millions)")
ax2.set_ylabel("Jeu")
st.pyplot(fig2)

# --- Ventes par année ---
st.subheader("📈 Ventes totales par année")
sales_by_year = df_filtered.groupby("Year")["Global_Sales"].sum()

fig3, ax3 = plt.subplots(figsize=(10, 4))
sales_by_year.plot(kind="line", marker="o", ax=ax3, color="royalblue")
ax3.set_ylabel("Ventes (millions)")
ax3.set_xlabel("Année")
st.pyplot(fig3)

# --- Note critique vs ventes (si dispo) ---
if "Critic_Score" in df.columns:
    st.subheader("🎯 Corrélation : note critique vs ventes")
    df_score = df_filtered.dropna(subset=["Critic_Score"])
    fig4, ax4 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=df_score, x="Critic_Score", y="Global_Sales", hue="Genre", ax=ax4)
    ax4.set_xlabel("Note Critique")
    ax4.set_ylabel("Ventes Globales")
    st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("👨‍💻 Réalisé avec Streamlit | Dataset : [Kaggle - Video Game Sales](https://www.kaggle.com/datasets/rush4ratio/video-game-sales-with-ratings)")
