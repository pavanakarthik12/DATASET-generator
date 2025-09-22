"""
Pexels API service
Handles image data requests
"""

import requests
from typing import Dict, Any, Optional, List
from config.config import config
from app.utils.helpers import handle_api_error

class PexelsService:
    """Service for Pexels API integration"""
    
    def __init__(self):
        self.api_key = config.PEXELS_API_KEY
        self.base_url = config.PEXELS_BASE_URL
    
    def search_photos(self, query: str, per_page: int = 15, page: int = 1,
                     orientation: Optional[str] = None, size: Optional[str] = None,
                     color: Optional[str] = None) -> Dict[str, Any]:
        """Search for photos"""
        try:
            if not self.api_key:
                return {"error": "Pexels API key not configured"}
            
            if not query.strip():
                return {"error": "Query cannot be empty"}
            
            url = f"{self.base_url}/search"
            headers = {
                "Authorization": self.api_key
            }
            params = {
                "query": query,
                "per_page": min(per_page, 80),  # API limit is 80
                "page": page
            }
            
            if orientation and orientation in ["landscape", "portrait", "square"]:
                params["orientation"] = orientation
            if size and size in ["large", "medium", "small"]:
                params["size"] = size
            if color and color in ["red", "orange", "yellow", "green", "turquoise", 
                                 "blue", "violet", "pink", "brown", "black", "gray", "white"]:
                params["color"] = color
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Pexels")
        except Exception as e:
            return handle_api_error(e, "Pexels")
    
    def get_curated_photos(self, per_page: int = 15, page: int = 1) -> Dict[str, Any]:
        """Get curated photos"""
        try:
            if not self.api_key:
                return {"error": "Pexels API key not configured"}
            
            url = f"{self.base_url}/curated"
            headers = {
                "Authorization": self.api_key
            }
            params = {
                "per_page": min(per_page, 80),
                "page": page
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Pexels")
        except Exception as e:
            return handle_api_error(e, "Pexels")
    
    def get_photo_by_id(self, photo_id: int) -> Dict[str, Any]:
        """Get a specific photo by ID"""
        try:
            if not self.api_key:
                return {"error": "Pexels API key not configured"}
            
            url = f"{self.base_url}/photos/{photo_id}"
            headers = {
                "Authorization": self.api_key
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Pexels")
        except Exception as e:
            return handle_api_error(e, "Pexels")
    
    def get_videos(self, query: str, per_page: int = 15, page: int = 1,
                   orientation: Optional[str] = None, size: Optional[str] = None,
                   min_duration: Optional[int] = None, max_duration: Optional[int] = None) -> Dict[str, Any]:
        """Search for videos"""
        try:
            if not self.api_key:
                return {"error": "Pexels API key not configured"}
            
            if not query.strip():
                return {"error": "Query cannot be empty"}
            
            url = f"{self.base_url}/videos/search"
            headers = {
                "Authorization": self.api_key
            }
            params = {
                "query": query,
                "per_page": min(per_page, 80),
                "page": page
            }
            
            if orientation and orientation in ["landscape", "portrait", "square"]:
                params["orientation"] = orientation
            if size and size in ["large", "medium", "small"]:
                params["size"] = size
            if min_duration:
                params["min_duration"] = min_duration
            if max_duration:
                params["max_duration"] = max_duration
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Pexels")
        except Exception as e:
            return handle_api_error(e, "Pexels")
    
    def get_popular_photos(self, per_page: int = 15, page: int = 1) -> Dict[str, Any]:
        """Get popular photos (using curated as proxy)"""
        return self.get_curated_photos(per_page, page)
    
    def search_photos_by_category(self, category: str, per_page: int = 15, page: int = 1) -> Dict[str, Any]:
        """Search photos by category"""
        category_queries = {
            "nature": "nature landscape forest mountain",
            "business": "business office corporate",
            "technology": "technology computer digital",
            "people": "people portrait human",
            "food": "food restaurant cuisine",
            "travel": "travel vacation destination",
            "sports": "sports fitness exercise",
            "animals": "animals wildlife pets",
            "architecture": "architecture building city",
            "abstract": "abstract art design"
        }
        
        if category.lower() not in category_queries:
            return {"error": f"Category '{category}' not supported"}
        
        query = category_queries[category.lower()]
        return self.search_photos(query, per_page, page)
    
    def get_photographer_photos(self, photographer_id: int, per_page: int = 15, page: int = 1) -> Dict[str, Any]:
        """Get photos by a specific photographer"""
        try:
            if not self.api_key:
                return {"error": "Pexels API key not configured"}
            
            url = f"{self.base_url}/v1/photos"
            headers = {
                "Authorization": self.api_key
            }
            params = {
                "photographer_id": photographer_id,
                "per_page": min(per_page, 80),
                "page": page
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Pexels")
        except Exception as e:
            return handle_api_error(e, "Pexels")
