"""
OpenWeatherMap API service
Handles weather data requests
"""

import requests
from typing import Dict, Any, Optional
from config.config import config
from app.utils.helpers import handle_api_error, validate_coordinates

class OpenWeatherService:
    """Service for OpenWeatherMap API integration"""
    
    def __init__(self):
        self.api_key = config.OPENWEATHER_API_KEY
        self.base_url = config.OPENWEATHER_BASE_URL
        
    def get_current_weather(self, city: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """Get current weather for a city"""
        try:
            if not self.api_key:
                return {"error": "OpenWeather API key not configured"}
            
            query = f"{city},{country_code}" if country_code else city
            url = f"{self.base_url}/weather"
            params = {
                "q": query,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "OpenWeatherMap")
        except Exception as e:
            return handle_api_error(e, "OpenWeatherMap")
    
    def get_weather_by_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get weather by coordinates"""
        try:
            if not self.api_key:
                return {"error": "OpenWeather API key not configured"}
            
            if not validate_coordinates(lat, lon):
                return {"error": "Invalid coordinates"}
            
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "OpenWeatherMap")
        except Exception as e:
            return handle_api_error(e, "OpenWeatherMap")
    
    def get_forecast(self, city: str, days: int = 5) -> Dict[str, Any]:
        """Get weather forecast"""
        try:
            if not self.api_key:
                return {"error": "OpenWeather API key not configured"}
            
            if days < 1 or days > 5:
                return {"error": "Days must be between 1 and 5"}
            
            url = f"{self.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "OpenWeatherMap")
        except Exception as e:
            return handle_api_error(e, "OpenWeatherMap")
    
    def get_historical_weather(self, lat: float, lon: float, date: str) -> Dict[str, Any]:
        """Get historical weather data (requires One Call API subscription)"""
        try:
            if not self.api_key:
                return {"error": "OpenWeather API key not configured"}
            
            if not validate_coordinates(lat, lon):
                return {"error": "Invalid coordinates"}
            
            # Note: This requires One Call API subscription
            url = f"{self.base_url}/onecall/timemachine"
            params = {
                "lat": lat,
                "lon": lon,
                "dt": int(date.replace("-", "")),
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "OpenWeatherMap")
        except Exception as e:
            return handle_api_error(e, "OpenWeatherMap")
