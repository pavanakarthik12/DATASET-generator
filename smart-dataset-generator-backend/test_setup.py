#!/usr/bin/env python3
"""
Quick setup test for Smart Dataset Generator Backend
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test FastAPI imports
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        print("✓ FastAPI imports successful")
        
        # Test service imports
        from app.services.openweather_service import OpenWeatherService
        from app.services.alphavantage_service import AlphaVantageService
        from app.services.newsapi_service import NewsAPIService
        from app.services.pexels_service import PexelsService
        from app.services.covid_service import COVIDService
        print("✓ Service imports successful")
        
        # Test route imports
        from app.routes import api_routes, chatbot_routes, download_routes
        print("✓ Route imports successful")
        
        # Test utility imports
        from app.utils.helpers import format_weather_data, save_to_csv
        print("✓ Utility imports successful")
        
        # Test config imports
        from config.config import config
        print("✓ Config imports successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from config.config import config
        
        # Check if API keys are loaded (they might be None if not set)
        print(f"Alpha Vantage API Key: {'✓ Set' if config.ALPHAVANTAGE_API_KEY else '✗ Not set'}")
        print(f"NewsAPI Key: {'✓ Set' if config.NEWSAPI_API_KEY else '✗ Not set'}")
        print(f"OpenWeather API Key: {'✓ Set' if config.OPENWEATHER_API_KEY else '✗ Not set'}")
        print(f"Pexels API Key: {'✓ Set' if config.PEXELS_API_KEY else '✗ Not set'}")
        print(f"OpenRouter API Key: {'✓ Set' if config.OPENROUTER_API_KEY else '✗ Not set'}")
        
        return True
        
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directories...")
    
    required_dirs = ["data", "data/temp", "app", "app/routes", "app/services", "app/utils", "config", "tests"]
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✓ {directory}")
        else:
            print(f"✗ {directory} - Creating...")
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✓ {directory} - Created")

def test_services():
    """Test service initialization"""
    print("\nTesting service initialization...")
    
    try:
        from app.services.openweather_service import OpenWeatherService
        from app.services.alphavantage_service import AlphaVantageService
        from app.services.newsapi_service import NewsAPIService
        from app.services.pexels_service import PexelsService
        from app.services.covid_service import COVIDService
        
        # Initialize services
        weather_service = OpenWeatherService()
        stock_service = AlphaVantageService()
        news_service = NewsAPIService()
        image_service = PexelsService()
        covid_service = COVIDService()
        
        print("✓ All services initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Service initialization error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("SMART DATASET GENERATOR - SETUP TEST")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test directories
    test_directories()
    
    # Test configuration
    if not test_config():
        all_tests_passed = False
    
    # Test services
    if not test_services():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Your Smart Dataset Generator Backend is ready to use!")
        print("\nTo start the server:")
        print("  python start.py")
        print("  or")
        print("  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix them before running the server.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
