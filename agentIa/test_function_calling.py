"""
Script de test pour le function calling
"""

from generateText import generateText, get_function_calling_prompt, process_llm_response, writeFile, launchPythonFile

def test_function_calling():
    """Test du function calling"""
    print("🧪 Test du Function Calling")
    print("=" * 50)
    
    # Test 1: Demander à l'IA de créer un fichier hello world
    print("\n1️⃣ Test de création d'un fichier hello world...")
    user_message = "Peux-tu créer un fichier hello.py qui contient un programme Python qui affiche 'Hello World'?"
    
    # Créer le prompt pour function calling
    prompt = get_function_calling_prompt(user_message)
    print(f"📝 Prompt envoyé : {prompt[:100]}...")
    
    try:
        # Générer la réponse
        response = generateText(prompt)
        print(f"🔄 Réponse brute du LLM : {response}")
        
        # Traiter la réponse
        final_response = process_llm_response(response, user_message)
        print(f"✅ Réponse finale : {final_response}")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
    
    # Test 2: Vérifier si le fichier a été créé
    print("\n2️⃣ Vérification de la création du fichier...")
    try:
        with open("hello.py", 'r') as f:
            content = f.read()
        print(f"✅ Fichier créé avec succès ! Contenu :\n{content}")
    except FileNotFoundError:
        print("❌ Fichier hello.py non trouvé")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")
    
    # Test 3: Lancer le fichier Python
    print("\n3️⃣ Test d'exécution du fichier Python...")
    try:
        result = launchPythonFile("hello.py")
        print(f"🚀 Résultat de l'exécution : {result}")
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution : {e}")

def test_direct_function_calls():
    """Test direct des fonctions"""
    print("\n🔧 Test direct des fonctions")
    print("=" * 30)
    
    # Test writeFile
    print("📝 Test writeFile...")
    result = writeFile("test.py", 'print("Hello from test file!")')
    print(f"Résultat : {result}")
    
    # Test launchPythonFile
    print("🚀 Test launchPythonFile...")
    result = launchPythonFile("test.py")
    print(f"Résultat : {result}")

if __name__ == "__main__":
    test_function_calling()
    test_direct_function_calls()
