import requests
import os
import json
import subprocess
from typing import Optional

# Utilisation d'une variable d'environnement pour plus de sécurité
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "dBirbmjBuFQLXfHvap8IfeDup2EkIemO")

def generateText(prompt: str, model: str = "mistral-tiny", temperature: float = 0.7, max_tokens: Optional[int] = None) -> str:
    """
    Génère du texte en utilisant l'API Mistral AI.
    
    Args:
        prompt: Le prompt à envoyer à l'API
        model: Le modèle à utiliser (mistral-tiny, mistral-small, mistral-medium, etc.)
        temperature: Contrôle la créativité (0.0 à 1.0)
        max_tokens: Limite le nombre de tokens dans la réponse
    
    Returns:
        Le texte généré par l'API
    
    Raises:
        Exception: Si l'API retourne une erreur
    """
    if not MISTRAL_API_KEY:
        raise ValueError("Clé API Mistral manquante. Définissez MISTRAL_API_KEY dans vos variables d'environnement.")
    
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }
    
    # Ajouter max_tokens seulement si spécifié
    if max_tokens is not None:
        data["max_tokens"] = max_tokens
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Vérification plus robuste de la structure de la réponse
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception("Structure de réponse inattendue de l'API Mistral")
        else:
            # Gestion d'erreurs plus détaillée
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


def chat_interface():
    """Interface de chat simple en ligne de commande avec function calling"""
    print("🤖 Assistant IA Mistral avec Function Calling - Tapez 'quit' pour quitter")
    print("📋 Fonctions disponibles : writeFile, launchPythonFile")
    print("=" * 60)
    
    while True:
        try:
            # Demander à l'utilisateur de taper quelque chose
            user_input = input("\n💬 Vous: ").strip()
            
            # Vérifier si l'utilisateur veut quitter
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("👋 Au revoir!")
                break
            
            # Vérifier si l'input n'est pas vide
            if not user_input:
                print("❌ Veuillez taper quelque chose...")
                continue
            
            # Créer le prompt pour function calling
            print("🤔 Réflexion en cours...")
            function_prompt = get_function_calling_prompt(user_input)
            
            # Générer la réponse
            response = generateText(function_prompt)
            
            # Traiter la réponse et exécuter les fonctions si nécessaire
            final_response = process_llm_response(response, user_input)
            
            print(f"🤖 Assistant: {final_response}")
            
        except KeyboardInterrupt:
            print("\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("🔄 Réessayez...")

def writeFile(path: str, content: str) -> str:
    """
    Écrit du contenu dans un fichier.
    
    Args:
        path: Le chemin du fichier à créer
        content: Le contenu à écrire dans le fichier
    
    Returns:
        Message de confirmation
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Fichier créé avec succès : {path}"
    except Exception as e:
        return f"❌ Erreur lors de la création du fichier : {str(e)}"

def launchPythonFile(path: str) -> str:
    """
    Lance un fichier Python.
    
    Args:
        path: Le chemin du fichier Python à exécuter
    
    Returns:
        Le résultat de l'exécution
    """
    try:
        result = subprocess.run(['python', path], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"✅ Exécution réussie :\n{result.stdout}"
        else:
            return f"❌ Erreur d'exécution :\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "⏱️ Timeout : Le script a pris trop de temps à s'exécuter"
    except Exception as e:
        return f"❌ Erreur lors du lancement : {str(e)}"

def get_function_calling_prompt(user_message: str) -> str:
    """
    Créé un prompt pour le function calling.
    
    Args:
        user_message: Le message de l'utilisateur
    
    Returns:
        Le prompt formaté pour le function calling
    """
    return f"""Tu es un assistant qui peut utiliser des fonctions. Tu as accès aux fonctions suivantes :

1. writeFile(path, content)
   - Crée un fichier avec le contenu spécifié
   - path: chemin du fichier (string)
   - content: contenu à écrire (string)

2. launchPythonFile(path)
   - Lance un fichier Python
   - path: chemin du fichier Python (string)

L'utilisateur dit: "{user_message}"

Si tu dois utiliser une fonction, réponds UNIQUEMENT avec un JSON valide dans ce format :
{{
    "function_name": "nom_de_la_fonction",
    "arguments": {{
        "argument1": "valeur1",
        "argument2": "valeur2"
    }}
}}

Si tu n'as pas besoin d'utiliser une fonction, réponds normalement.

Ne réponds QUE avec le JSON ou un texte normal, pas les deux."""

def execute_function_call(function_name: str, arguments: dict) -> str:
    """
    Exécute une fonction basée sur son nom et ses arguments.
    
    Args:
        function_name: Le nom de la fonction à exécuter
        arguments: Les arguments à passer à la fonction
    
    Returns:
        Le résultat de l'exécution de la fonction
    """
    available_functions = {
        "writeFile": writeFile,
        "launchPythonFile": launchPythonFile
    }
    
    if function_name not in available_functions:
        return f"❌ Fonction inconnue : {function_name}"
    
    try:
        function = available_functions[function_name]
        result = function(**arguments)
        return result
    except Exception as e:
        return f"❌ Erreur lors de l'exécution de {function_name} : {str(e)}"

def process_llm_response(response: str, original_message: str) -> str:
    """
    Traite la réponse du LLM et exécute les fonctions si nécessaire.
    
    Args:
        response: La réponse du LLM
        original_message: Le message original de l'utilisateur
    
    Returns:
        Le résultat final
    """
    # Essayer de parser la réponse comme JSON
    try:
        response_json = json.loads(response.strip())
        
        # Vérifier si c'est un appel de fonction
        if "function_name" in response_json and "arguments" in response_json:
            function_name = response_json["function_name"]
            arguments = response_json["arguments"]
            
            print(f"🔧 Exécution de la fonction : {function_name}")
            print(f"📝 Arguments : {arguments}")
            
            # Exécuter la fonction
            result = execute_function_call(function_name, arguments)
            
            # Demander au LLM de commenter le résultat
            comment_prompt = f"""L'utilisateur a demandé : "{original_message}"
J'ai exécuté la fonction {function_name} avec les arguments {arguments}.
Résultat : {result}

Donne une réponse courte et amicale à l'utilisateur pour lui expliquer ce qui s'est passé."""
            
            try:
                comment = generateText(comment_prompt)
                return f"{result}\n\n🤖 {comment}"
            except:
                return result
        else:
            return response
    except json.JSONDecodeError:
        # Si ce n'est pas du JSON, c'est une réponse normale
        return response

# Exemple d'utilisation
if __name__ == "__main__":
    chat_interface()
