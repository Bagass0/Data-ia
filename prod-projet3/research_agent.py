import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
from urllib.parse import urlparse
import re
from duckduckgo_search import DDGS
import streamlit as st
from mistralai import Mistral
import json

class IntelligentResearchAgent:
    """Agent de recherche intelligent avec LLM Mistral et scraping réel"""
    
    def __init__(self, mistral_api_key: str = "ALtuLSeq8ppLELjJT5OAF8Qda5YBCsWA"):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Initialisation du client Mistral
        self.mistral_client = Mistral(api_key=mistral_api_key)
        self.model = "mistral-small-latest"  # Modèle le plus performant
        
    def generate_search_plan_with_llm(self, query: str) -> Dict[str, Any]:
        """Génère un plan de recherche intelligent avec Mistral AI"""
        
        try:
            # Prompt pour Mistral AI
            prompt = f"""
Analyse cette requête de recherche et génère un plan de recherche intelligent au format JSON.

Requête: "{query}"

Tu dois analyser l'intention de la requête et retourner un plan structuré avec:
1. L'intention détectée (comparison_shopping, price_research, news_research, tutorial_research, general_research)
2. Les sites cibles recommandés selon l'intention
3. Les stratégies de recherche
4. Les variantes de requêtes à utiliser

Format de réponse attendu (JSON uniquement):
{{
    "query": "{query}",
    "analysis": {{
        "intent": "type_d_intention",
        "keywords": ["mot1", "mot2", "mot3"],
        "context": "description_du_contexte"
    }},
    "target_sites": [
        {{"name": "Nom_du_site", "url": "domaine.com", "search_type": "type"}},
        {{"name": "Autre_site", "url": "general", "search_type": "type"}}
    ],
    "search_queries": [
        "{query}",
        "variante_1",
        "variante_2"
    ],
    "search_strategy": [
        "strategie_1",
        "strategie_2"
    ]
}}

Réponds uniquement avec le JSON, sans texte additionnel.
"""

            # Appel à Mistral AI
            messages = [{"role": "user", "content": prompt}]
            
            response = self.mistral_client.chat.complete(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            
            # Extraction et parsing de la réponse JSON
            response_content = response.choices[0].message.content.strip()
            
            # Nettoyage de la réponse pour extraire le JSON
            if "```json" in response_content:
                response_content = response_content.split("```json")[1].split("```")[0]
            elif "```" in response_content:
                response_content = response_content.split("```")[1]
            
            plan = json.loads(response_content)
            
            # Validation et enrichissement du plan
            if "analysis" not in plan:
                plan["analysis"] = {"intent": "general_research"}
            if "target_sites" not in plan:
                plan["target_sites"] = [{"name": "Sites généralistes", "url": "general", "search_type": "general"}]
            if "search_queries" not in plan:
                plan["search_queries"] = [query]
            if "search_strategy" not in plan:
                plan["search_strategy"] = [f"Rechercher '{query}' sur moteurs généralistes"]
            
            return plan
            
        except Exception as e:
            st.warning(f"Erreur LLM Mistral, utilisation du fallback: {str(e)}")
            # Fallback vers l'ancienne méthode
            return self._generate_fallback_plan(query)
    
    def _generate_fallback_plan(self, query: str) -> Dict[str, Any]:
        """Plan de recherche fallback si Mistral AI échoue"""
        plan = {
            "query": query,
            "analysis": {},
            "search_strategy": [],
            "target_sites": [],
            "search_queries": []
        }
        
        # Analyse de la requête
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['meilleur', 'top', 'comparaison', 'test', 'avis']):
            plan["analysis"]["intent"] = "comparison_shopping"
            plan["target_sites"] = [
                {"name": "Amazon", "url": "amazon.fr", "search_type": "product"},
                {"name": "Cdiscount", "url": "cdiscount.com", "search_type": "product"},
                {"name": "Articles de test", "url": "general", "search_type": "articles"}
            ]
            
        elif any(word in query_lower for word in ['prix', 'coût', 'tarif', 'budget']):
            plan["analysis"]["intent"] = "price_research"
            plan["target_sites"] = [
                {"name": "Sites de prix", "url": "general", "search_type": "price"},
                {"name": "Forums", "url": "general", "search_type": "discussion"}
            ]
            
        elif any(word in query_lower for word in ['actualité', 'news', 'nouveau']):
            plan["analysis"]["intent"] = "news_research"
            plan["target_sites"] = [
                {"name": "Sites d'actualités", "url": "general", "search_type": "news"},
                {"name": "Blogs spécialisés", "url": "general", "search_type": "blog"}
            ]
            
        elif any(word in query_lower for word in ['comment', 'guide', 'tutoriel', 'apprendre']):
            plan["analysis"]["intent"] = "tutorial_research"
            plan["target_sites"] = [
                {"name": "Sites tutoriels", "url": "general", "search_type": "tutorial"},
                {"name": "YouTube", "url": "youtube.com", "search_type": "video"},
                {"name": "Forums techniques", "url": "general", "search_type": "forum"}
            ]
        else:
            plan["analysis"]["intent"] = "general_research"
            plan["target_sites"] = [
                {"name": "Sites généralistes", "url": "general", "search_type": "general"}
            ]
        
        # Génération des requêtes de recherche
        plan["search_queries"] = [
            query,
            f"{query} avis",
            f"{query} comparaison",
            f"{query} 2025"
        ]
        
        # Stratégie de recherche
        plan["search_strategy"] = [
            f"Rechercher '{query}' sur moteurs généralistes",
            f"Analyser les sites e-commerce pour '{query}'",
            f"Collecter les avis et comparaisons",
            f"Synthétiser les informations trouvées"
        ]
        
        return plan
    
    def search_web(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Recherche web réelle avec DuckDuckGo"""
        try:
            with DDGS() as ddgs:
                results = []
                search_results = ddgs.text(query, max_results=max_results)
                
                for i, result in enumerate(search_results):
                    if i >= max_results:
                        break
                        
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                        "source": self._extract_domain(result.get("href", "")),
                        "relevance_score": 1.0 - (i * 0.1)
                    })
                
                return results
                
        except Exception as e:
            st.error(f"Erreur lors de la recherche web: {e}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extrait le domaine d'une URL"""
        try:
            return urlparse(url).netloc.replace('www.', '')
        except:
            return "inconnu"
    
    def scrape_content(self, url: str) -> Dict[str, Any]:
        """Scrappe le contenu d'une page web"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Suppression des scripts et styles
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extraction du titre
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Titre non trouvé"
            
            # Extraction du contenu principal
            content_selectors = [
                'article', 'main', '.content', '#content', '.post', '.article',
                'div[role="main"]', '.main-content', '.entry-content'
            ]
            
            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(separator=' ', strip=True)
                    break
            
            if not content:
                # Fallback: prendre tout le texte du body
                body = soup.find('body')
                if body:
                    content = body.get_text(separator=' ', strip=True)
            
            # Limitation de la taille du contenu
            content = content[:5000] if len(content) > 5000 else content
            
            return {
                "url": url,
                "title": title_text,
                "content": content,
                "word_count": len(content.split()),
                "status": "success"
            }
            
        except requests.exceptions.Timeout:
            return {
                "url": url,
                "title": "Timeout",
                "content": "Le site a mis trop de temps à répondre",
                "status": "timeout"
            }
        except requests.exceptions.RequestException as e:
            return {
                "url": url,
                "title": "Erreur de connexion",
                "content": f"Impossible d'accéder au site: {str(e)}",
                "status": "error"
            }
        except Exception as e:
            return {
                "url": url,
                "title": "Erreur de parsing",
                "content": f"Erreur lors de l'analyse du contenu: {str(e)}",
                "status": "error"
            }
    
    def filter_relevant_sites(self, search_results: List[Dict], target_sites: List[Dict]) -> List[Dict]:
        """Filtre les résultats selon les sites cibles du plan"""
        filtered_results = []
        
        for result in search_results:
            url = result.get("url", "")
            domain = self._extract_domain(url)
            
            # Vérification si le site correspond aux cibles
            is_relevant = False
            for target in target_sites:
                target_url = target.get("url", "")
                if target_url == "general" or target_url in domain:
                    is_relevant = True
                    result["target_type"] = target.get("search_type", "general")
                    break
            
            # Filtrage par type de contenu
            if self._is_relevant_content(result, target_sites):
                is_relevant = True
            
            if is_relevant:
                filtered_results.append(result)
        
        return filtered_results[:8]  # Limite à 8 résultats
    
    def _is_relevant_content(self, result: Dict, target_sites: List[Dict]) -> bool:
        """Vérifie si le contenu est pertinent selon les types de sites cibles"""
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()
        
        for target in target_sites:
            search_type = target.get("search_type", "")
            
            if search_type == "product" and any(word in title + snippet for word in ['test', 'avis', 'comparaison', 'meilleur']):
                return True
            elif search_type == "news" and any(word in title + snippet for word in ['actualité', 'nouveau', '2025', '2024']):
                return True
            elif search_type == "tutorial" and any(word in title + snippet for word in ['guide', 'comment', 'tutoriel', 'apprendre']):
                return True
        
        return False
    
    def synthesize_with_llm(self, query: str, scraped_contents: List[Dict]) -> Dict[str, Any]:
        """Synthétise les résultats avec Mistral AI"""
        
        if not scraped_contents:
            return {
                "summary": "Aucun contenu n'a pu être analysé pour cette recherche.",
                "key_points": [],
                "recommendations": [],
                "sources_summary": "Aucune source accessible",
                "confidence": 0.1
            }
        
        try:
            # Préparation du contenu pour Mistral AI
            content_summary = ""
            successful_scrapes = 0
            source_titles = []
            
            for content in scraped_contents:
                if content.get("status") == "success" and content.get("content"):
                    # Limitation du contenu pour éviter de dépasser les tokens
                    content_text = content.get("content", "")[:1000]
                    title = content.get("title", "")
                    url = content.get("url", "")
                    
                    content_summary += f"\n--- Source: {title} ({url}) ---\n{content_text}\n"
                    source_titles.append(title)
                    successful_scrapes += 1
            
            if not content_summary:
                return self._generate_fallback_summary(query, scraped_contents)
            
            # Prompt pour Mistral AI
            prompt = f"""
Analyse le contenu scrapé suivant et génère une synthèse intelligente pour la requête: "{query}"

Contenu des sources web:
{content_summary}

Tu dois créer une synthèse au format JSON avec:
1. Un résumé clair et informatif
2. 3-5 points clés extraits du contenu
3. 2-3 recommandations pratiques
4. Un score de confiance (0.0 à 1.0)

Format de réponse (JSON uniquement):
{{
    "summary": "Résumé détaillé et informatif basé sur les sources analysées",
    "key_points": [
        "Point clé 1 extrait du contenu",
        "Point clé 2 avec informations concrètes",
        "Point clé 3 pertinent"
    ],
    "recommendations": [
        "Recommandation pratique 1",
        "Recommandation pratique 2"
    ],
    "confidence": 0.8,
    "sources_summary": "{successful_scrapes} sources analysées avec succès"
}}

Réponds uniquement avec le JSON, sans texte additionnel.
"""

            # Appel à Mistral AI
            messages = [{"role": "user", "content": prompt}]
            
            response = self.mistral_client.chat.complete(
                model=self.model,
                messages=messages,
                temperature=0.4,
                max_tokens=800
            )
            
            # Extraction et parsing de la réponse JSON
            response_content = response.choices[0].message.content.strip()
            
            # Nettoyage de la réponse pour extraire le JSON
            if "```json" in response_content:
                response_content = response_content.split("```json")[1].split("```")[0]
            elif "```" in response_content:
                response_content = response_content.split("```")[1]
            
            synthesis = json.loads(response_content)
            
            # Validation des champs requis
            required_fields = ["summary", "key_points", "recommendations", "confidence"]
            for field in required_fields:
                if field not in synthesis:
                    if field == "summary":
                        synthesis[field] = f"Analyse de {successful_scrapes} sources sur '{query}'"
                    elif field == "key_points":
                        synthesis[field] = ["Informations trouvées dans les sources analysées"]
                    elif field == "recommendations":
                        synthesis[field] = ["Consultez les sources pour plus de détails"]
                    elif field == "confidence":
                        synthesis[field] = 0.6
            
            synthesis["sources_summary"] = f"{successful_scrapes} sources analysées avec succès"
            
            return synthesis
            
        except Exception as e:
            st.warning(f"Erreur lors de la synthèse Mistral AI: {str(e)}")
            return self._generate_fallback_summary(query, scraped_contents)
    
    def _generate_fallback_summary(self, query: str, scraped_contents: List[Dict]) -> Dict[str, Any]:
        """Synthèse fallback si Mistral AI échoue"""
        successful_scrapes = 0
        all_content = ""
        
        for content in scraped_contents:
            if content.get("status") == "success":
                all_content += content.get("content", "") + " "
                successful_scrapes += 1
        
        # Génération simple basée sur le contenu
        query_words = [word.lower() for word in query.split() if len(word) > 2]
        
        summary = f"Basé sur l'analyse de {successful_scrapes} sources, voici ce que j'ai trouvé sur '{query}': "
        if all_content:
            sentences = [s.strip() for s in all_content.split('.') if len(s.strip()) > 20]
            relevant_sentences = [s for s in sentences[:10] if any(word in s.lower() for word in query_words)]
            if relevant_sentences:
                summary += relevant_sentences[0][:200] + "..."
        
        return {
            "summary": summary,
            "key_points": [
                f"Informations collectées depuis {successful_scrapes} sources web",
                "Contenu analysé automatiquement",
                "Résultats basés sur le scraping en temps réel"
            ],
            "recommendations": [
                "Consultez les sources originales pour plus de détails",
                "Vérifiez les informations sur plusieurs sites"
            ],
            "confidence": min(0.8, successful_scrapes * 0.15 + 0.2),
            "sources_summary": f"{successful_scrapes} sources analysées avec succès"
        }
    
    def _generate_intelligent_summary(self, query: str, content: str, query_words: List[str], successful_scrapes: int, source_count: int) -> Dict[str, Any]:
        """Génère une synthèse intelligente basée sur le contenu"""
        
        # Analyse du contenu pour extraire des informations pertinentes
        content_lower = content.lower()
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        
        # Recherche de phrases pertinentes
        relevant_sentences = []
        for sentence in sentences[:50]:  # Limite à 50 phrases
            sentence_lower = sentence.lower()
            if any(word in sentence_lower for word in query_words):
                relevant_sentences.append(sentence)
        
        # Extraction de points clés
        key_points = []
        if "meilleur" in query.lower():
            key_points.extend(self._extract_product_info(content))
        elif "prix" in query.lower():
            key_points.extend(self._extract_price_info(content))
        elif "comment" in query.lower():
            key_points.extend(self._extract_tutorial_info(content))
        
        # Génération du résumé principal
        if relevant_sentences:
            summary = f"Basé sur l'analyse de {source_count} sources, voici ce que j'ai trouvé sur '{query}': "
            summary += " ".join(relevant_sentences[:3])
        else:
            summary = f"L'analyse de {source_count} sources révèle des informations variées sur '{query}'. "
            summary += "Les sources consultées offrent différentes perspectives sur le sujet."
        
        # Recommandations
        recommendations = self._generate_recommendations(query, content)
        
        return {
            "summary": summary,
            "key_points": key_points[:5],  # Max 5 points
            "recommendations": recommendations[:3],  # Max 3 recommandations
            "sources_summary": f"{source_count} sources analysées avec succès",
            "confidence": min(0.9, successful_scrapes * 0.1 + 0.3) if successful_scrapes > 0 else 0.3
        }
    
    def _extract_product_info(self, content: str) -> List[str]:
        """Extrait des informations sur les produits"""
        points = []
        content_lower = content.lower()
        
        if "amazon" in content_lower:
            points.append("Produits disponibles sur Amazon avec avis clients")
        if "prix" in content_lower or "€" in content or "$" in content:
            points.append("Informations de prix trouvées")
        if "avis" in content_lower or "test" in content_lower:
            points.append("Tests et avis d'utilisateurs disponibles")
        
        return points
    
    def _extract_price_info(self, content: str) -> List[str]:
        """Extrait des informations sur les prix"""
        points = []
        
        # Recherche de prix dans le contenu
        price_patterns = [r'\d+[,.]?\d*\s*€', r'\d+[,.]?\d*\s*euros?']
        for pattern in price_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                points.append("Informations de tarification détaillées trouvées")
                break
        
        return points
    
    def _extract_tutorial_info(self, content: str) -> List[str]:
        """Extrait des informations tutorielles"""
        points = []
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["étape", "step", "guide", "tutoriel"]):
            points.append("Guide étape par étape disponible")
        if any(word in content_lower for word in ["exemple", "exemple", "démo"]):
            points.append("Exemples pratiques fournis")
        
        return points
    
    def _generate_recommendations(self, query: str, content: str) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []
        content_lower = content.lower()
        query_lower = query.lower()
        
        if "meilleur" in query_lower:
            recommendations.append("Comparez les avis utilisateurs avant votre choix")
            recommendations.append("Vérifiez les prix sur plusieurs sites")
        
        if "prix" in query_lower:
            recommendations.append("Surveillez les promotions et offres spéciales")
        
        if "amazon" in content_lower:
            recommendations.append("Consultez Amazon pour plus d'options et d'avis")
        
        return recommendations
    
    def full_research(self, query: str) -> Dict[str, Any]:
        """Processus complet de recherche intelligente"""
        
        # 1. Génération du plan avec LLM
        research_plan = self.generate_search_plan_with_llm(query)
        
        # 2. Recherche web
        search_results = []
        for search_query in research_plan["search_queries"][:3]:  # Limite à 3 requêtes
            results = self.search_web(search_query, max_results=5)
            search_results.extend(results)
        
        # 3. Filtrage selon le plan
        filtered_results = self.filter_relevant_sites(search_results, research_plan["target_sites"])
        
        # 4. Scraping des sites pertinents
        scraped_contents = []
        for result in filtered_results[:6]:  # Limite à 6 sites
            content = self.scrape_content(result["url"])
            content["search_result"] = result
            scraped_contents.append(content)
        
        # 5. Synthèse avec LLM
        synthesis = self.synthesize_with_llm(query, scraped_contents)
        
        return {
            "query": query,
            "research_plan": research_plan,
            "search_results": filtered_results,
            "scraped_contents": scraped_contents,
            "synthesis": synthesis,
            "timestamp": time.time()
        }
