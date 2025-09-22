"""
Alpha Vantage API service
Handles stock market data requests
"""

import requests
from typing import Dict, Any, Optional
from config.config import config
from app.utils.helpers import handle_api_error

class AlphaVantageService:
    """Service for Alpha Vantage API integration"""
    
    def __init__(self):
        self.api_key = config.ALPHAVANTAGE_API_KEY
        self.base_url = config.ALPHAVANTAGE_BASE_URL
    
    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time stock quote"""
        try:
            if not self.api_key:
                return {"error": "Alpha Vantage API key not configured"}
            
            url = self.base_url
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol.upper(),
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Alpha Vantage")
        except Exception as e:
            return handle_api_error(e, "Alpha Vantage")
    
    def get_daily_stock_data(self, symbol: str, outputsize: str = "compact") -> Dict[str, Any]:
        """Get daily stock data"""
        try:
            if not self.api_key:
                return {"error": "Alpha Vantage API key not configured"}
            
            if outputsize not in ["compact", "full"]:
                return {"error": "Output size must be 'compact' or 'full'"}
            
            url = self.base_url
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol.upper(),
                "outputsize": outputsize,
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Alpha Vantage")
        except Exception as e:
            return handle_api_error(e, "Alpha Vantage")
    
    def get_weekly_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get weekly stock data"""
        try:
            if not self.api_key:
                return {"error": "Alpha Vantage API key not configured"}
            
            url = self.base_url
            params = {
                "function": "TIME_SERIES_WEEKLY",
                "symbol": symbol.upper(),
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Alpha Vantage")
        except Exception as e:
            return handle_api_error(e, "Alpha Vantage")
    
    def get_monthly_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get monthly stock data"""
        try:
            if not self.api_key:
                return {"error": "Alpha Vantage API key not configured"}
            
            url = self.base_url
            params = {
                "function": "TIME_SERIES_MONTHLY",
                "symbol": symbol.upper(),
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Alpha Vantage")
        except Exception as e:
            return handle_api_error(e, "Alpha Vantage")
    
    def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company overview and fundamentals"""
        try:
            if not self.api_key:
                return {"error": "Alpha Vantage API key not configured"}
            
            url = self.base_url
            params = {
                "function": "OVERVIEW",
                "symbol": symbol.upper(),
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Alpha Vantage")
        except Exception as e:
            return handle_api_error(e, "Alpha Vantage")
    
    def get_earnings_calendar(self, symbol: str) -> Dict[str, Any]:
        """Get earnings calendar for a symbol"""
        try:
            if not self.api_key:
                return {"error": "Alpha Vantage API key not configured"}
            
            url = self.base_url
            params = {
                "function": "EARNINGS_CALENDAR",
                "symbol": symbol.upper(),
                "horizon": "3month",
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Alpha Vantage")
        except Exception as e:
            return handle_api_error(e, "Alpha Vantage")
    
    def get_forex_rates(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Get foreign exchange rates"""
        try:
            if not self.api_key:
                return {"error": "Alpha Vantage API key not configured"}
            
            url = self.base_url
            params = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_currency.upper(),
                "to_currency": to_currency.upper(),
                "apikey": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "Alpha Vantage")
        except Exception as e:
            return handle_api_error(e, "Alpha Vantage")
