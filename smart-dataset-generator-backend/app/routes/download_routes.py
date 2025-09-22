"""
Download routes for dataset exports
Handles CSV, JSON, Parquet, and ZIP file downloads
"""

from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import FileResponse
from typing import Optional, List, Dict, Any
import os
import tempfile
from datetime import datetime
from app.services.openweather_service import OpenWeatherService
from app.services.alphavantage_service import AlphaVantageService
from app.services.newsapi_service import NewsAPIService
from app.services.pexels_service import PexelsService
from app.services.covid_service import COVIDService
from app.utils.helpers import (
    save_to_csv, save_to_json, save_to_parquet, download_images,
    cleanup_temp_file, format_weather_data, format_stock_data,
    format_news_data, format_image_data
)

router = APIRouter()

# Initialize services
weather_service = OpenWeatherService()
stock_service = AlphaVantageService()
news_service = NewsAPIService()
image_service = PexelsService()
covid_service = COVIDService()

@router.get("/weather/csv")
async def download_weather_csv(
    city: str = Query(..., description="City name"),
    country_code: Optional[str] = Query(None, description="Country code")
):
    """Download weather data as CSV"""
    try:
        # Get weather data
        data = weather_service.get_current_weather(city, country_code)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data for CSV
        formatted_data = format_weather_data(data)
        csv_data = [formatted_data]
        
        # Create CSV file
        file_path = save_to_csv(csv_data, f"weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            media_type="text/csv",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/json")
async def download_weather_json(
    city: str = Query(..., description="City name"),
    country_code: Optional[str] = Query(None, description="Country code")
):
    """Download weather data as JSON"""
    try:
        # Get weather data
        data = weather_service.get_current_weather(city, country_code)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data
        formatted_data = format_weather_data(data)
        
        # Create JSON file
        file_path = save_to_json(formatted_data, f"weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            media_type="application/json",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/csv/{symbol}")
async def download_stocks_csv(
    symbol: str = Path(..., description="Stock symbol"),
    outputsize: str = Query("compact", description="Output size: compact or full")
):
    """Download stock data as CSV"""
    try:
        # Get stock data
        data = stock_service.get_daily_stock_data(symbol, outputsize)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data for CSV
        formatted_data = format_stock_data(data)
        csv_data = formatted_data.get("data", [])
        
        if not csv_data:
            raise HTTPException(status_code=400, detail="No stock data available")
        
        # Create CSV file
        file_path = save_to_csv(csv_data, f"stocks_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"stocks_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            media_type="text/csv",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stocks/parquet/{symbol}")
async def download_stocks_parquet(
    symbol: str = Path(..., description="Stock symbol"),
    outputsize: str = Query("compact", description="Output size: compact or full")
):
    """Download stock data as Parquet"""
    try:
        # Get stock data
        data = stock_service.get_daily_stock_data(symbol, outputsize)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data for Parquet
        formatted_data = format_stock_data(data)
        parquet_data = formatted_data.get("data", [])
        
        if not parquet_data:
            raise HTTPException(status_code=400, detail="No stock data available")
        
        # Create Parquet file
        file_path = save_to_parquet(parquet_data, f"stocks_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"stocks_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet",
            media_type="application/octet-stream",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/csv")
async def download_news_csv(
    query: str = Query(..., description="Search query"),
    language: str = Query("en", description="Language code"),
    page_size: int = Query(20, description="Number of articles")
):
    """Download news data as CSV"""
    try:
        # Get news data
        data = news_service.search_news(query, language, page_size=page_size)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data for CSV
        formatted_data = format_news_data(data)
        csv_data = formatted_data.get("articles", [])
        
        if not csv_data:
            raise HTTPException(status_code=400, detail="No news data available")
        
        # Create CSV file
        file_path = save_to_csv(csv_data, f"news_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"news_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            media_type="text/csv",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/news/json")
async def download_news_json(
    query: str = Query(..., description="Search query"),
    language: str = Query("en", description="Language code"),
    page_size: int = Query(20, description="Number of articles")
):
    """Download news data as JSON"""
    try:
        # Get news data
        data = news_service.search_news(query, language, page_size=page_size)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data
        formatted_data = format_news_data(data)
        
        # Create JSON file
        file_path = save_to_json(formatted_data, f"news_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"news_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            media_type="application/json",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/zip")
async def download_images_zip(
    query: str = Query(..., description="Search query"),
    per_page: int = Query(10, description="Number of images"),
    orientation: Optional[str] = Query(None, description="Image orientation")
):
    """Download images as ZIP file"""
    try:
        # Get image data
        data = image_service.search_photos(query, per_page, orientation=orientation)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data
        formatted_data = format_image_data(data)
        photos = formatted_data.get("photos", [])
        
        if not photos:
            raise HTTPException(status_code=400, detail="No images available")
        
        # Extract image URLs
        image_urls = [photo.get("src", {}).get("original", "") for photo in photos if photo.get("src", {}).get("original")]
        
        if not image_urls:
            raise HTTPException(status_code=400, detail="No valid image URLs found")
        
        # Create ZIP file
        file_path = download_images(image_urls, f"images_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"images_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            media_type="application/zip",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/covid/csv/{country}")
async def download_covid_csv(
    country: str = Path(..., description="Country name or code")
):
    """Download COVID-19 data as CSV"""
    try:
        # Get COVID data
        data = covid_service.get_country_data(country)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Format data for CSV
        if isinstance(data, list):
            csv_data = data
        else:
            csv_data = [data]
        
        # Create CSV file
        file_path = save_to_csv(csv_data, f"covid_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"covid_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            media_type="text/csv",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/covid/json/{country}")
async def download_covid_json(
    country: str = Path(..., description="Country name or code")
):
    """Download COVID-19 data as JSON"""
    try:
        # Get COVID data
        data = covid_service.get_country_data(country)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        # Create JSON file
        file_path = save_to_json(data, f"covid_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"covid_{country}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            media_type="application/json",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/combined/csv")
async def download_combined_csv(
    weather_city: Optional[str] = Query(None, description="City for weather data"),
    stock_symbol: Optional[str] = Query(None, description="Stock symbol"),
    news_query: Optional[str] = Query(None, description="News search query"),
    covid_country: Optional[str] = Query(None, description="Country for COVID data")
):
    """Download combined data from multiple sources as CSV"""
    try:
        combined_data = []
        
        # Get weather data
        if weather_city:
            weather_data = weather_service.get_current_weather(weather_city)
            if "error" not in weather_data:
                formatted_weather = format_weather_data(weather_data)
                combined_data.append({"source": "weather", "data": formatted_weather})
        
        # Get stock data
        if stock_symbol:
            stock_data = stock_service.get_daily_stock_data(stock_symbol)
            if "error" not in stock_data:
                formatted_stock = format_stock_data(stock_data)
                combined_data.append({"source": "stocks", "data": formatted_stock})
        
        # Get news data
        if news_query:
            news_data = news_service.search_news(news_query, page_size=10)
            if "error" not in news_data:
                formatted_news = format_news_data(news_data)
                combined_data.append({"source": "news", "data": formatted_news})
        
        # Get COVID data
        if covid_country:
            covid_data = covid_service.get_country_data(covid_country)
            if "error" not in covid_data:
                combined_data.append({"source": "covid", "data": covid_data})
        
        if not combined_data:
            raise HTTPException(status_code=400, detail="No data available for the specified parameters")
        
        # Create CSV file
        file_path = save_to_csv(combined_data, f"combined_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        
        # Return file response
        return FileResponse(
            path=file_path,
            filename=f"combined_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            media_type="text/csv",
            background=lambda: cleanup_temp_file(file_path)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
