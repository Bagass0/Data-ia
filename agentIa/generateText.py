"""
Agent IA avec Function Calling et exécution multi-étapes
Utilise l'API Mistral AI pour générer du texte et exécuter des actions
"""

import json
import os
import subprocess
import requests
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
DEFAULT_MODEL = "mistral-tiny"
DEFAULT_TEMPERATURE = 0.7
API_TIMEOUT = 30
SCRIPT_TIMEOUT = 30


def generateText(prompt: str, model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE, max_tokens: Optional[int] = None) -> str:
    """
    Génère du texte en utilisant l'API Mistral AI.
    
    Args:
        prompt: Le prompt à envoyer à l'API
        model: Le modèle à utiliser
        temperature: Contrôle la créativité (0.0 à 1.0)
        max_tokens: Limite le nombre de tokens
    
    Returns:
        Le texte généré par l'API
    
    Raises:
        Exception: Si l'API retourne une erreur
    """
    if not MISTRAL_API_KEY:
        raise ValueError("Clé API Mistral manquante dans le fichier .env")
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    
    if max_tokens is not None:
        data["max_tokens"] = max_tokens
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=API_TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("Structure de réponse inattendue de l'API Mistral")
        else:
            error_msg = f"Erreur API Mistral: {response.status_code}"
            try:
                error_details = response.json()
                if "error" in error_details:
                    error_msg += f" - {error_details['error']}"
            except:
                error_msg += f" - {response.text}"
            raise Exception(error_msg)
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erreur de connexion à l'API Mistral: {str(e)}")


def writeFile(path: str, content: str) -> str:
    """
    Écrit du contenu dans un fichier dans le dossier 'generated'.
    
    Args:
        path: Le chemin du fichier à créer (sera placé dans generated/)
        content: Le contenu à écrire
    
    Returns:
        Message de confirmation
    """
    try:
        # Créer le dossier generated s'il n'existe pas
        generated_dir = "generated"
        if not os.path.exists(generated_dir):
            os.makedirs(generated_dir)
        
        # Construire le chemin complet dans le dossier generated
        full_path = os.path.join(generated_dir, path)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Fichier créé avec succès : {full_path}"
    except Exception as e:
        return f"❌ Erreur lors de la création du fichier : {str(e)}"


def launchPythonFile(path: str) -> str:
    """
    Lance un fichier Python depuis le dossier 'generated'.
    
    Args:
        path: Le chemin du fichier Python à exécuter
    
    Returns:
        Le résultat de l'exécution
    """
    try:
        # Normaliser le chemin - enlever les "generated/" en double
        if path.startswith("generated/") or path.startswith("generated\\"):
            # Le chemin contient déjà generated/, on l'utilise tel quel
            full_path = path.replace("\\", "/")  # Normaliser les séparateurs
        else:
            # Ajouter generated/ devant
            generated_dir = "generated"
            full_path = os.path.join(generated_dir, path).replace("\\", "/")
        
        # Vérifier que le fichier existe
        if not os.path.exists(full_path):
            # Essayer aussi sans le préfixe generated/ au cas où
            alt_path = path
            if os.path.exists(alt_path):
                full_path = alt_path
            else:
                return f"❌ Fichier non trouvé : {full_path} (aussi testé: {alt_path})"
        
        result = subprocess.run(['python', full_path], capture_output=True, text=True, timeout=SCRIPT_TIMEOUT)
        if result.returncode == 0:
            return f"✅ Exécution réussie :\n{result.stdout}"
        else:
            return f"❌ Erreur d'exécution :\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "⏱️ Timeout : Le script a pris trop de temps à s'exécuter"
    except Exception as e:
        return f"❌ Erreur lors du lancement : {str(e)}"


def readFile(path: str) -> str:
    """
    Lit le contenu d'un fichier depuis le dossier 'generated'.
    
    Args:
        path: Le chemin du fichier à lire
    
    Returns:
        Le contenu du fichier ou un message d'erreur
    """
    try:
        # Normaliser le chemin - enlever les "generated/" en double
        if path.startswith("generated/") or path.startswith("generated\\"):
            # Le chemin contient déjà generated/, on l'utilise tel quel
            full_path = path.replace("\\", "/")
        else:
            # Ajouter generated/ devant
            generated_dir = "generated"
            full_path = os.path.join(generated_dir, path).replace("\\", "/")
        
        # Vérifier que le fichier existe
        if not os.path.exists(full_path):
            # Essayer aussi sans le préfixe generated/ au cas où
            alt_path = path
            if os.path.exists(alt_path):
                full_path = alt_path
            else:
                return f"❌ Fichier non trouvé : {full_path}"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"✅ Contenu du fichier {full_path} :\n{content}"
    except Exception as e:
        return f"❌ Erreur lors de la lecture du fichier : {str(e)}"


def stop() -> str:
    """
    Fonction pour arrêter l'agent.
    
    Returns:
        Message d'arrêt
    """
    return "🛑 Agent arrêté - Tâche terminée"


class Agent:
    """Agent IA avec capacité d'exécution multi-étapes"""
    
    def __init__(self):
        self.available_functions = {
            "writeFile": writeFile,
            "launchPythonFile": launchPythonFile,
            "readFile": readFile,
            "stop": stop
        }
        self.execution_history = []
    
    def get_function_calling_prompt(self, user_message: str, history: List[str] = None) -> str:
        """
        Créé un prompt pour le function calling avec historique.
        
        Args:
            user_message: Le message de l'utilisateur
            history: Historique des actions précédentes
        
        Returns:
            Le prompt formaté
        """
        history_text = ""
        if history:
            history_text = f"\n\nHistorique des actions précédentes :\n" + "\n".join(history)
        
        return f"""Tu es un assistant qui peut utiliser des fonctions pour accomplir des tâches complexes.

Fonctions disponibles :

1. writeFile(path, content)
   - Crée un fichier avec le contenu spécifié
   - path: chemin du fichier (string)
   - content: contenu à écrire (string)

2. launchPythonFile(path)
   - Lance un fichier Python
   - path: chemin du fichier Python (string)

3. readFile(path)
   - Lit le contenu d'un fichier
   - path: chemin du fichier (string)

4. stop()
   - Arrête l'agent quand la tâche est terminée
   - Aucun argument requis

Demande de l'utilisateur: "{user_message}"{history_text}

Si tu dois utiliser une fonction, réponds UNIQUEMENT avec un JSON valide dans ce format :
{{
    "function_name": "nom_de_la_fonction",
    "arguments": {{
        "argument1": "valeur1",
        "argument2": "valeur2"
    }}
}}

Si la tâche est terminée, utilise la fonction "stop".
Si tu n'as pas besoin d'utiliser une fonction maintenant, réponds normalement.

Ne réponds QUE avec le JSON ou un texte normal, pas les deux."""

    def execute_function_call(self, function_name: str, arguments: Dict) -> str:
        """
        Exécute une fonction basée sur son nom et ses arguments.
        
        Args:
            function_name: Le nom de la fonction à exécuter
            arguments: Les arguments à passer à la fonction
        
        Returns:
            Le résultat de l'exécution
        """
        if function_name not in self.available_functions:
            return f"❌ Fonction inconnue : {function_name}"
        
        try:
            function = self.available_functions[function_name]
            if arguments:
                result = function(**arguments)
            else:
                result = function()
            return result
        except Exception as e:
            return f"❌ Erreur lors de l'exécution de {function_name} : {str(e)}"

    def process_llm_response(self, response: str, step: int) -> tuple:
        """
        Traite la réponse du LLM et exécute les fonctions si nécessaire.
        
        Args:
            response: La réponse du LLM
            step: Numéro de l'étape
        
        Returns:
            Tuple (résultat, should_stop)
        """
        try:
            response_json = json.loads(response.strip())
            
            if "function_name" in response_json and "arguments" in response_json:
                function_name = response_json["function_name"]
                arguments = response_json.get("arguments", {})
                
                print(f"🔧 Étape {step}: Exécution de la fonction : {function_name}")
                print(f"� Arguments : {arguments}")
                
                # Exécuter la fonction
                result = self.execute_function_call(function_name, arguments)
                
                # Ajouter à l'historique
                history_entry = f"Étape {step}: {function_name}({arguments}) -> {result}"
                self.execution_history.append(history_entry)
                
                # Vérifier si c'est la fonction stop
                should_stop = function_name == "stop"
                
                return result, should_stop
            else:
                return response, False
        except json.JSONDecodeError:
            # Si ce n'est pas du JSON, c'est une réponse normale
            return response, False

    def run_agent(self, prompt: str, max_step: int = 10) -> List[str]:
        """
        Lance l'agent pour accomplir une tâche avec plusieurs étapes.
        
        Args:
            prompt: La demande initiale de l'utilisateur
            max_step: Nombre maximum d'étapes
        
        Returns:
            Liste des résultats de chaque étape
        """
        print(f"🚀 Démarrage de l'agent pour : {prompt}")
        print(f"📊 Maximum {max_step} étapes")
        print("=" * 60)
        
        results = []
        self.execution_history = []
        
        for step in range(1, max_step + 1):
            print(f"\n🎯 ÉTAPE {step}/{max_step}")
            print("-" * 30)
            
            # Créer le prompt avec l'historique
            function_prompt = self.get_function_calling_prompt(prompt, self.execution_history)
            
            try:
                # Générer la réponse
                print("🤔 Réflexion en cours...")
                response = generateText(function_prompt)
                
                # Traiter la réponse
                result, should_stop = self.process_llm_response(response, step)
                results.append(result)
                
                print(f"� Résultat : {result}")
                
                # Vérifier si l'agent veut s'arrêter
                if should_stop:
                    print(f"\n🏁 Agent arrêté à l'étape {step}")
                    break
                    
            except Exception as e:
                error_msg = f"❌ Erreur à l'étape {step}: {str(e)}"
                print(error_msg)
                results.append(error_msg)
                break
        
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DE L'EXÉCUTION")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"Étape {i}: {result}")
        
        return results


def chat_interface():
    """Interface de chat avec l'agent"""
    print("🤖 Agent IA Mistral avec Function Calling Multi-Étapes")
    print("📋 Fonctions disponibles : writeFile, launchPythonFile, stop")
    print("🔄 Commandes spéciales :")
    print("   - 'agent <demande>' : Lance l'agent multi-étapes")
    print("   - 'quit' : Quitter")
    print("=" * 60)
    
    agent = Agent()
    
    while True:
        try:
            user_input = input("\n💬 Vous: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("👋 Au revoir!")
                break
            
            if not user_input:
                print("❌ Veuillez taper quelque chose...")
                continue
            
            # Vérifier si c'est une demande d'agent multi-étapes
            if user_input.lower().startswith('agent '):
                task = user_input[6:]  # Enlever 'agent '
                max_steps = 5  # Par défaut 5 étapes
                agent.run_agent(task, max_steps)
            else:
                # Utilisation normale du chat
                print("🤔 Réflexion en cours...")
                response = generateText(user_input)
                print(f"🤖 Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("🔄 Réessayez...")


if __name__ == "__main__":
    chat_interface()
