"""
Configuration management for Smart Dataset Generator
Loads environment variables safely
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings"""
    
    # API Keys
    ALPHAVANTAGE_API_KEY: Optional[str] = os.getenv("ALPHAVANTAGE_API_KEY")
    NEWSAPI_API_KEY: Optional[str] = os.getenv("NEWSAPI_API_KEY")
    OPENWEATHER_API_KEY: Optional[str] = os.getenv("OPENWEATHER_API_KEY")
    PEXELS_API_KEY: Optional[str] = os.getenv("PEXELS_API_KEY")
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    
    # API URLs
    OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
    ALPHAVANTAGE_BASE_URL = "https://www.alphavantage.co/query"
    NEWSAPI_BASE_URL = "https://newsapi.org/v2"
    PEXELS_BASE_URL = "https://api.pexels.com/v1"
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    COVID_API_BASE_URL = "https://api.covid19api.com"
    
    # File storage
    DATA_DIR = "data"
    TEMP_DIR = "data/temp"
    
    # Rate limiting (requests per minute)
    RATE_LIMIT = 60
    
    @classmethod
    def validate_api_keys(cls) -> dict:
        """Validate that all required API keys are present"""
        missing_keys = []
        
        if not cls.ALPHAVANTAGE_API_KEY:
            missing_keys.append("ALPHAVANTAGE_API_KEY")
        if not cls.NEWSAPI_API_KEY:
            missing_keys.append("NEWSAPI_API_KEY")
        if not cls.OPENWEATHER_API_KEY:
            missing_keys.append("OPENWEATHER_API_KEY")
        if not cls.PEXELS_API_KEY:
            missing_keys.append("PEXELS_API_KEY")
        if not cls.OPENROUTER_API_KEY:
            missing_keys.append("OPENROUTER_API_KEY")
            
        return {
            "valid": len(missing_keys) == 0,
            "missing_keys": missing_keys
        }

# Create global config instance
config = Config()
