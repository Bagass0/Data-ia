import requests
import os
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
    """Interface de chat simple en ligne de commande"""
    print("🤖 Assistant IA Mistral - Tapez 'quit' pour quitter")
    print("=" * 50)
    
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
            
            # Générer la réponse
            print("🤔 Réflexion en cours...")
            response = generateText(user_input)
            print(f"🤖 Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Au revoir!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("🔄 Réessayez...")

# Exemple d'utilisation
if __name__ == "__main__":
    chat_interface()
