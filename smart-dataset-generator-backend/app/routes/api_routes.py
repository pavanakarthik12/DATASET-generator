"""
API routes for external data sources
Handles OpenWeatherMap, Alpha Vantage, NewsAPI, Pexels, and COVID-19 endpoints
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List
from app.services.openweather_service import OpenWeatherService
from app.services.alphavantage_service import AlphaVantageService
from app.services.newsapi_service import NewsAPIService
from app.services.pexels_service import PexelsService
from app.services.covid_service import COVIDService
from app.utils.helpers import (
    format_weather_data, format_stock_data, format_news_data, 
    format_image_data, validate_coordinates, validate_date_range
)

router = APIRouter()

# Initialize services
weather_service = OpenWeatherService()
stock_service = AlphaVantageService()
news_service = NewsAPIService()
image_service = PexelsService()
covid_service = COVIDService()

# Weather endpoints
@router.get("/weather/current")
async def get_current_weather(
    city: str = Query(..., description="City name"),
    country_code: Optional[str] = Query(None, description="Country code (e.g., 'US')")
):
    """Get current weather for a city"""
    try:
        data = weather_service.get_current_weather(city, country_code)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_weather_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/coordinates")
async def get_weather_by_coordinates(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get weather by coordinates"""
    try:
        if not validate_coordinates(lat, lon):
            raise HTTPException(status_code=400, detail="Invalid coordinates")
        
        data = weather_service.get_weather_by_coordinates(lat, lon)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_weather_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/forecast")
async def get_weather_forecast(
    city: str = Query(..., description="City name"),
    days: int = Query(5, description="Number of days (1-5)")
):
    """Get weather forecast. Returns OpenWeather 3-hourly forecast list (up to ~40 entries)."""
    try:
        if days < 1 or days > 5:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 5")
        
        data = weather_service.get_forecast(city, days)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Return raw forecast data with 'list' to match frontend expectations
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Stock market endpoints
@router.get("/stocks/quote/{symbol}")
async def get_stock_quote(symbol: str = Path(..., description="Stock symbol")):
    """Get real-time stock quote"""
    try:
        data = stock_service.get_stock_quote(symbol)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/daily/{symbol}")
async def get_daily_stock_data(
    symbol: str = Path(..., description="Stock symbol"),
    outputsize: str = Query("compact", description="Output size: compact or full")
):
    """Get daily stock data"""
    try:
        data = stock_service.get_daily_stock_data(symbol, outputsize)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_stock_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/company/{symbol}")
async def get_company_overview(symbol: str = Path(..., description="Stock symbol")):
    """Get company overview and fundamentals"""
    try:
        data = stock_service.get_company_overview(symbol)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# News endpoints
@router.get("/news/headlines")
async def get_top_headlines(
    country: str = Query("us", description="Country code"),
    category: Optional[str] = Query(None, description="News category"),
    page_size: int = Query(20, description="Number of articles")
):
    """Get top news headlines"""
    try:
        data = news_service.get_top_headlines(country, category, page_size)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_news_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/search")
async def search_news(
    query: str = Query(..., description="Search query"),
    language: str = Query("en", description="Language code"),
    page_size: int = Query(20, description="Number of articles")
):
    """Search for news articles"""
    try:
        data = news_service.search_news(query, language, page_size=page_size)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_news_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/trending")
async def get_trending_topics(
    country: str = Query("us", description="Country code"),
    category: str = Query("general", description="News category")
):
    """Get trending topics"""
    try:
        data = news_service.get_trending_topics(country, category)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Image endpoints
@router.get("/images/search")
async def search_images(
    query: str = Query(..., description="Search query"),
    per_page: int = Query(15, description="Number of images"),
    orientation: Optional[str] = Query(None, description="Image orientation"),
    color: Optional[str] = Query(None, description="Image color")
):
    """Search for images"""
    try:
        data = image_service.search_photos(query, per_page, orientation=orientation, color=color)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_image_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/curated")
async def get_curated_images(
    per_page: int = Query(15, description="Number of images")
):
    """Get curated images"""
    try:
        data = image_service.get_curated_photos(per_page)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_image_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/category/{category}")
async def get_images_by_category(
    category: str = Path(..., description="Image category"),
    per_page: int = Query(15, description="Number of images")
):
    """Get images by category"""
    try:
        data = image_service.search_photos_by_category(category, per_page)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        formatted_data = format_image_data(data)
        return {"success": True, "data": formatted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# COVID-19 endpoints
@router.get("/covid/global")
async def get_global_covid_data():
    """Get global COVID-19 summary"""
    try:
        data = covid_service.get_global_summary()
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/covid/country/{country}")
async def get_country_covid_data(
    country: str = Path(..., description="Country name or code")
):
    """Get COVID-19 data for a specific country"""
    try:
        data = covid_service.get_country_data(country)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/covid/top-countries")
async def get_top_countries_by_cases(
    limit: int = Query(10, description="Number of countries to return")
):
    """Get top countries by COVID-19 cases"""
    try:
        data = covid_service.get_top_countries_by_cases(limit)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/covid/countries")
async def get_available_countries():
    """Get list of available countries for COVID-19 data"""
    try:
        data = covid_service.get_countries_list()
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
