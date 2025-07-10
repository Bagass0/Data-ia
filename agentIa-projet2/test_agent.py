#!/usr/bin/env python3
"""
Script de test simple pour l'agent
"""

from generateText import Agent, generateText, writeFile, launchPythonFile

def test_basic_functions():
    """Test des fonctions de base avec dossier generated"""
    print("🧪 Test des fonctions de base (dossier generated)")
    print("-" * 40)
    
    try:
        # Test writeFile - fichier ira dans generated/
        result = writeFile('test_hello.py', 'print("Hello from Agent in generated folder!")')
        print(f"writeFile: {result}")
        
        # Test launchPythonFile - cherche dans generated/
        result = launchPythonFile('test_hello.py')
        print(f"launchPythonFile: {result}")
        
        print("✅ Fonctions de base OK")
        return True
    except Exception as e:
        print(f"❌ Erreur dans les fonctions de base: {e}")
        return False

def test_agent_simulation():
    """Test de l'agent avec simulation (sans API) - fichiers dans generated/"""
    print("\n🧪 Test de l'agent (simulation) - dossier generated")
    print("-" * 40)
    
    try:
        agent = Agent()
        
        # Test de création d'un simple fichier
        print("Test: Création et exécution d'un fichier simple dans generated/")
        
        # Simuler les étapes manuellement
        # Étape 1: Créer un fichier dans generated/
        result1 = writeFile('calcul_simple.py', 'result = 2 + 2\nprint(f"2 + 2 = {result}")')
        print(f"Étape 1 - Création: {result1}")
        
        # Étape 2: Exécuter le fichier depuis generated/
        result2 = launchPythonFile('calcul_simple.py')
        print(f"Étape 2 - Exécution: {result2}")
        
        print("✅ Test simulation OK")
        return True
    except Exception as e:
        print(f"❌ Erreur dans le test simulation: {e}")
        return False

def test_agent_real():
    """Test de l'agent réel avec API (optionnel)"""
    print("\n🧪 Test de l'agent réel avec API")
    print("-" * 40)
    
    try:
        agent = Agent()
        print("⚠️  Test avec API Mistral - Cela nécessite une clé API valide")
        
        # Test simple
        task = "Créer un fichier hello_api.py qui affiche 'Hello API dans generated!' et l'exécuter"
        print(f"Tâche: {task}")
        
        # Lancer l'agent (limité à 2 étapes pour le test)
        results = agent.run_agent(task, max_step=2)
        
        print(f"✅ Agent terminé avec {len(results)} résultats")
        return True
        
    except Exception as e:
        print(f"⚠️  Erreur API (normal si clé invalide): {e}")
        return False

if __name__ == "__main__":
    print("🚀 TEST DE L'AGENT IA")
    print("=" * 50)
    
    # Tests de base
    test1 = test_basic_functions()
    test2 = test_agent_simulation()
    
    # Test avec API (peut échouer si clé invalide)
    print("\n" + "=" * 50)
    print("🌐 TEST AVEC API (optionnel)")
    test3 = test_agent_real()
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    tests_passed = sum([test1, test2])
    total_core_tests = 2
    
    print(f"✅ Tests de base: {tests_passed}/{total_core_tests}")
    if test3:
        print("✅ Test API: Réussi")
    else:
        print("⚠️  Test API: Échoué (normal si clé API invalide)")
    
    if tests_passed == total_core_tests:
        print("\n🎉 TOUS LES TESTS DE BASE SONT RÉUSSIS!")
        print("Votre agent est prêt à utiliser!")
    else:
        print("\n❌ Certains tests ont échoué")
    
    print("\n📖 Pour utiliser l'agent:")
    print("   python generateText.py")
    print("   Puis tapez: agent <votre demande>")
