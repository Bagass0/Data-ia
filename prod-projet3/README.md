# 🔍 Agent de Recherche Intelligent

Agent de recherche moderne qui utilise un LLM pour générer un plan de recherche, puis scrappe des sites web réels pour fournir une synthèse intelligente.

## 🏗️ Architecture

```
prod-projet3/
├── research_agent.py       # 🧠 Agent de recherche avec LLM + scraping
├── research_app.py         # � Interface Streamlit moderne
├── requirements.txt        # 📦 Dépendances
└── README.md              # 📖 Documentation
```

## 🚀 Installation et lancement

```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement de l'application
streamlit run research_app.py
```

**Accès :** http://localhost:8501

## 🧠 Fonctionnement de l'Agent

### 1. 📝 Plan LLM Intelligent
L'agent analyse votre requête et détermine :
- **Intent** : Type de recherche (comparaison, prix, tutoriel, actualités...)
- **Sites cibles** : Amazon, forums, sites d'actualités selon le besoin
- **Stratégies** : Méthodes de recherche adaptées

### 2. 🌐 Recherche Web Réelle
- Utilise **DuckDuckGo** pour la recherche
- Filtre les résultats selon le plan LLM
- Sélectionne les sites les plus pertinents

### 3. 📖 Scraping Intelligent
- Extrait le contenu réel des sites web
- Parse HTML avec BeautifulSoup
- Gère les erreurs et timeouts

### 4. 🤖 Synthèse IA
- Analyse le contenu scrapé
- Génère un résumé intelligent
- Extrait les points clés et recommandations

## 🎯 Exemples de recherches

| Type | Exemple | Sites ciblés |
|------|---------|--------------|
| �️ **Produits** | "meilleurs casques moto 2025" | Amazon, Cdiscount, tests |
| 💰 **Prix** | "prix immobilier Paris" | Sites immobiliers, forums |
| � **Tutoriels** | "comment apprendre Python" | Sites éducatifs, YouTube |
| � **Actualités** | "actualités IA 2025" | Sites d'actualités, blogs |

## 🛠️ Technologies utilisées

- **Streamlit** - Interface web moderne
- **DuckDuckGo Search** - Recherche web réelle
- **BeautifulSoup4** - Parsing HTML
- **Requests** - HTTP et scraping
- **Intelligence artificielle** - Analyse et synthèse

## � Fonctionnalités Interface

- ✅ Design moderne et responsive
- ✅ Recherche en temps réel avec progress
- ✅ Plan LLM visible et détaillé
- ✅ Contenu scrapé affiché par source
- ✅ Métriques de qualité (confiance, pertinence)
- ✅ Synthèse intelligente avec recommandations
- ✅ Exemples interactifs

## 🔧 Configuration avancée

L'agent peut être étendu pour :
- Intégrer des APIs LLM réelles (OpenAI, Claude...)
- Ajouter plus de sources de données
- Implémenter du caching intelligent
- Ajouter des filtres de contenu

---

*� Agent de Recherche Intelligent - LLM + Scraping Réel*
