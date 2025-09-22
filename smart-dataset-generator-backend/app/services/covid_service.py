"""
COVID-19 API service
Handles COVID-19 data requests
"""

import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from config.config import config
from app.utils.helpers import handle_api_error

class COVIDService:
    """Service for COVID-19 API integration"""
    
    def __init__(self):
        self.base_url = config.COVID_API_BASE_URL
    
    def get_global_summary(self) -> Dict[str, Any]:
        """Get global COVID-19 summary"""
        try:
            url = f"{self.base_url}/summary"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "COVID-19 API")
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_country_data(self, country: str) -> Dict[str, Any]:
        """Get COVID-19 data for a specific country"""
        try:
            url = f"{self.base_url}/country/{country}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "COVID-19 API")
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_country_data_by_date(self, country: str, from_date: str, to_date: str) -> Dict[str, Any]:
        """Get COVID-19 data for a country within a date range"""
        try:
            url = f"{self.base_url}/country/{country}"
            params = {
                "from": from_date,
                "to": to_date
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "COVID-19 API")
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_world_data_by_date(self, from_date: str, to_date: str) -> Dict[str, Any]:
        """Get world COVID-19 data within a date range"""
        try:
            url = f"{self.base_url}/world"
            params = {
                "from": from_date,
                "to": to_date
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "COVID-19 API")
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_countries_list(self) -> Dict[str, Any]:
        """Get list of available countries"""
        try:
            url = f"{self.base_url}/countries"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "COVID-19 API")
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_live_data_by_country(self, country: str) -> Dict[str, Any]:
        """Get live COVID-19 data for a country"""
        try:
            url = f"{self.base_url}/live/country/{country}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "COVID-19 API")
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_live_data_world(self) -> Dict[str, Any]:
        """Get live COVID-19 data for the world"""
        try:
            url = f"{self.base_url}/live"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "COVID-19 API")
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_statistics_by_country(self, country: str) -> Dict[str, Any]:
        """Get comprehensive statistics for a country"""
        try:
            # Get current data
            current_data = self.get_country_data(country)
            if "error" in current_data:
                return current_data
            
            # Get live data
            live_data = self.get_live_data_by_country(country)
            if "error" in live_data:
                return live_data
            
            # Combine data
            return {
                "country": country,
                "current_data": current_data,
                "live_data": live_data,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_top_countries_by_cases(self, limit: int = 10) -> Dict[str, Any]:
        """Get top countries by total cases"""
        try:
            summary = self.get_global_summary()
            if "error" in summary:
                return summary
            
            countries = summary.get("Countries", [])
            if not countries:
                return {"error": "No country data available"}
            
            # Sort by total confirmed cases
            sorted_countries = sorted(
                countries, 
                key=lambda x: x.get("TotalConfirmed", 0), 
                reverse=True
            )
            
            return {
                "top_countries": sorted_countries[:limit],
                "total_countries": len(countries),
                "last_updated": summary.get("Date", "")
            }
            
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
    
    def get_vaccination_data(self, country: str) -> Dict[str, Any]:
        """Get vaccination data (if available)"""
        try:
            # Note: This is a placeholder as the free COVID-19 API doesn't include vaccination data
            # In a real implementation, you would use a different API or data source
            return {
                "message": "Vaccination data not available in free tier",
                "country": country,
                "suggestion": "Use a dedicated vaccination API for this data"
            }
            
        except Exception as e:
            return handle_api_error(e, "COVID-19 API")
