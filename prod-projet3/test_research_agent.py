"""
Test de l'agent de recherche
"""

from research_agent import ResearchAgent
import json

def test_research_agent():
    """Test complet de l'agent de recherche"""
    agent = ResearchAgent()
    
    # Test de requêtes différentes
    test_queries = [
        "actualités intelligence artificielle",
        "qu'est-ce que le machine learning",
        "comment créer une startup",
        "prix immobilier Paris 2025"
    ]
    
    print("🔍 Test de l'Agent de Recherche")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 30)
        
        # Recherche complète
        results = agent.full_research(query)
        
        # Affichage des résultats
        print(f"Type de requête: {results['query_analysis']['query_type']}")
        print(f"Mots-clés: {', '.join(results['query_analysis']['keywords'])}")
        print(f"Nombre de résultats: {results['synthesis']['total_results']}")
        print(f"Confiance: {results['synthesis']['confidence']:.1%}")
        print(f"Résumé: {results['synthesis']['summary'][:100]}...")
        
        # Sources
        print("Sources trouvées:")
        for j, source in enumerate(results['synthesis']['sources'], 1):
            print(f"  {j}. {source['title']} ({source['source']})")

def test_individual_functions():
    """Test des fonctions individuelles"""
    agent = ResearchAgent()
    query = "actualités intelligence artificielle"
    
    print("\n🧪 Test des fonctions individuelles")
    print("=" * 40)
    
    # Test analyse de requête
    print("\n1. Analyse de requête:")
    analysis = agent.understand_query(query)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    # Test plan de recherche
    print("\n2. Plan de recherche:")
    plan = agent.generate_research_plan(analysis)
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    
    # Test recherche web
    print("\n3. Recherche web:")
    results = agent.execute_web_search(query, max_results=2)
    for result in results:
        print(f"- {result['title']}")
        print(f"  Source: {result['source']}")
        print(f"  Contenu: {result['content'][:100]}...")

if __name__ == "__main__":
    test_research_agent()
    test_individual_functions()
