# 🤖 Agent IA Mistral avec Function Calling

Agent intelligent capable d'exécuter des tâches complexes en plusieurs étapes avec l'API Mistral AI.

## 🚀 Fonctionnalités

- **generateText(prompt)** : Génère du texte via l'API Mistral
- **Function Calling** : Exécute des fonctions (writeFile, launchPythonFile, stop)
- **Agent Multi-Étapes** : Exécute des tâches complexes en plusieurs étapes avec historique
- **Arrêt Intelligent** : L'agent peut décider quand arrêter une tâche

## 📋 Installation

1. Installer les dépendances :
```bash
pip install requests python-dotenv
```

2. Le fichier `.env` est déjà configuré avec la clé API.

## 🎯 Utilisation

### Interface de Chat

```bash
python generateText.py
```

**Commandes disponibles :**
- `agent <tâche>` : Lance l'agent multi-étapes
- `<question>` : Chat simple avec Mistral
- `quit` : Quitter

### Exemples d'utilisation

```
💬 Vous: agent Créer un fichier hello.py qui affiche Hello World et l'exécuter

💬 Vous: agent Faire un script qui calcule la factorielle de 5 et l'exécuter

💬 Vous: Explique-moi Python
```

### Utilisation Programmatique

```python
from generateText import Agent, generateText

# Agent multi-étapes
agent = Agent()
results = agent.run_agent("Créer un script Python et l'exécuter", max_step=5)

# Génération de texte simple
response = generateText("Explique-moi les listes en Python")
```

## 🔧 Fonctions Disponibles

- **writeFile(path, content)** : Crée un fichier dans le dossier `generated/`
- **launchPythonFile(path)** : Exécute un fichier Python depuis le dossier `generated/`
- **stop()** : Arrête l'agent

## 📁 Organisation des Fichiers

Tous les fichiers générés par l'agent sont automatiquement placés dans le dossier `generated/` pour garder le projet organisé :

## 🧪 Test

```bash
python test_agent.py
```

## 📁 Structure du Projet

```
agentIa/
├── .env                # Clé API Mistral
├── generateText.py     # Agent principal
├── test_agent.py       # Tests
├── README.md          # Documentation
└── generated/         # 📂 Tous les fichiers créés par l'agent
    ├── hello.py
    ├── calcul.py
    └── ...
```

## 🎯 Exemple de Workflow Agent

1. L'utilisateur donne une tâche
2. L'agent analyse et décompose la tâche
3. Exécute les actions nécessaires (écriture/exécution de fichiers)
4. Garde un historique des actions
5. Décide quand arrêter avec la fonction `stop`

L'agent est maintenant prêt à utiliser ! 🚀
