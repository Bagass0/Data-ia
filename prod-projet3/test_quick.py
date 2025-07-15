"""
Test rapide de l'agent de recherche intelligent
"""

from research_agent import IntelligentResearchAgent

def test_agent():
    print("🔍 Test de l'Agent de Recherche Intelligent")
    print("=" * 50)
    
    agent = IntelligentResearchAgent()
    
    # Test avec une requête simple
    query = "meilleurs casques moto 2025"
    print(f"\n📝 Test avec: '{query}'")
    print("-" * 30)
    
    # Test du plan LLM
    plan = agent.generate_search_plan_with_llm(query)
    print(f"Intent détecté: {plan['analysis']['intent']}")
    print(f"Sites cibles: {len(plan['target_sites'])}")
    
    # Test de recherche web
    print("\n🌐 Test recherche web...")
    results = agent.search_web(query, max_results=3)
    print(f"Résultats trouvés: {len(results)}")
    
    if results:
        print("Premier résultat:")
        print(f"- Titre: {results[0]['title'][:50]}...")
        print(f"- URL: {results[0]['url']}")

if __name__ == "__main__":
    test_agent()
