"""
NewsAPI service
Handles news data requests
"""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from config.config import config
from app.utils.helpers import handle_api_error

class NewsAPIService:
    """Service for NewsAPI integration"""
    
    def __init__(self):
        self.api_key = config.NEWSAPI_API_KEY
        self.base_url = config.NEWSAPI_BASE_URL
    
    def get_top_headlines(self, country: str = "us", category: Optional[str] = None, 
                         sources: Optional[str] = None, q: Optional[str] = None, 
                         page_size: int = 20) -> Dict[str, Any]:
        """Get top headlines"""
        try:
            if not self.api_key:
                return {"error": "NewsAPI key not configured"}
            
            url = f"{self.base_url}/top-headlines"
            params = {
                "apiKey": self.api_key,
                "country": country,
                "pageSize": min(page_size, 100)  # API limit is 100
            }
            
            if category:
                params["category"] = category
            if sources:
                params["sources"] = sources
            if q:
                params["q"] = q
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "NewsAPI")
        except Exception as e:
            return handle_api_error(e, "NewsAPI")
    
    def search_news(self, query: str, language: str = "en", sort_by: str = "publishedAt",
                   from_date: Optional[str] = None, to_date: Optional[str] = None,
                   page_size: int = 20, page: int = 1) -> Dict[str, Any]:
        """Search for news articles"""
        try:
            if not self.api_key:
                return {"error": "NewsAPI key not configured"}
            
            if not query.strip():
                return {"error": "Query cannot be empty"}
            
            url = f"{self.base_url}/everything"
            params = {
                "apiKey": self.api_key,
                "q": query,
                "language": language,
                "sortBy": sort_by,
                "pageSize": min(page_size, 100),
                "page": page
            }
            
            if from_date:
                params["from"] = from_date
            if to_date:
                params["to"] = to_date
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "NewsAPI")
        except Exception as e:
            return handle_api_error(e, "NewsAPI")
    
    def get_sources(self, category: Optional[str] = None, language: str = "en",
                   country: Optional[str] = None) -> Dict[str, Any]:
        """Get available news sources"""
        try:
            if not self.api_key:
                return {"error": "NewsAPI key not configured"}
            
            url = f"{self.base_url}/sources"
            params = {
                "apiKey": self.api_key,
                "language": language
            }
            
            if category:
                params["category"] = category
            if country:
                params["country"] = country
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "NewsAPI")
        except Exception as e:
            return handle_api_error(e, "NewsAPI")
    
    def get_news_by_domain(self, domains: List[str], page_size: int = 20) -> Dict[str, Any]:
        """Get news from specific domains"""
        try:
            if not self.api_key:
                return {"error": "NewsAPI key not configured"}
            
            if not domains:
                return {"error": "At least one domain must be specified"}
            
            url = f"{self.base_url}/everything"
            params = {
                "apiKey": self.api_key,
                "domains": ",".join(domains),
                "pageSize": min(page_size, 100),
                "sortBy": "publishedAt"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "NewsAPI")
        except Exception as e:
            return handle_api_error(e, "NewsAPI")
    
    def get_news_by_keywords(self, keywords: List[str], language: str = "en",
                           page_size: int = 20) -> Dict[str, Any]:
        """Get news by keywords"""
        try:
            if not self.api_key:
                return {"error": "NewsAPI key not configured"}
            
            if not keywords:
                return {"error": "At least one keyword must be specified"}
            
            # Create query from keywords
            query = " OR ".join(keywords)
            
            url = f"{self.base_url}/everything"
            params = {
                "apiKey": self.api_key,
                "q": query,
                "language": language,
                "pageSize": min(page_size, 100),
                "sortBy": "relevancy"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "NewsAPI")
        except Exception as e:
            return handle_api_error(e, "NewsAPI")
    
    def get_trending_topics(self, country: str = "us", category: str = "general") -> Dict[str, Any]:
        """Get trending topics (simulated by getting top headlines)"""
        try:
            if not self.api_key:
                return {"error": "NewsAPI key not configured"}
            
            # Get top headlines to identify trending topics
            headlines = self.get_top_headlines(country=country, category=category, page_size=50)
            
            if "error" in headlines:
                return headlines
            
            # Extract keywords from headlines (simple implementation)
            articles = headlines.get("articles", [])
            trending_keywords = []
            
            for article in articles[:10]:  # Analyze top 10 articles
                title = article.get("title", "").lower()
                # Simple keyword extraction (in production, use NLP)
                words = title.split()
                trending_keywords.extend([word for word in words if len(word) > 4])
            
            return {
                "trending_keywords": list(set(trending_keywords))[:20],
                "articles_count": len(articles),
                "country": country,
                "category": category
            }
            
        except Exception as e:
            return handle_api_error(e, "NewsAPI")
