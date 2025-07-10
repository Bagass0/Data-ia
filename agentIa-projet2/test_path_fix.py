#!/usr/bin/env python3
"""
Test rapide du problème de double chemin
"""

from generateText import writeFile, launchPythonFile, readFile

def test_path_fix():
    print("🧪 Test de correction du problème de chemin")
    print("-" * 50)
    
    # Créer un fichier de test
    print("1. Création d'un fichier de test...")
    result = writeFile('test_path.py', 'print("Test de chemin réussi!")')
    print(f"   {result}")
    
    # Essayer de l'exécuter (problème précédent)
    print("\n2. Exécution du fichier...")
    result = launchPythonFile('test_path.py')
    print(f"   {result}")
    
    # Tester la lecture
    print("\n3. Lecture du fichier...")
    result = readFile('test_path.py')
    print(f"   {result}")
    
    # Test avec chemin complet (cas problématique)
    print("\n4. Test avec chemin generated/ explicite...")
    result = launchPythonFile('generated/test_path.py')
    print(f"   {result}")

if __name__ == "__main__":
    test_path_fix()
