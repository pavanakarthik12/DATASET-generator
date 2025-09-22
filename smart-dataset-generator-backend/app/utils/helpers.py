"""
Helper utilities for Smart Dataset Generator
Common functions for validation, formatting, and file operations
"""

import os
import json
import csv
import pandas as pd
import tempfile
import zipfile
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
import requests
from pathlib import Path

def create_temp_file(extension: str = ".json") -> str:
    """Create a temporary file and return its path"""
    temp_dir = Path("data/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    temp_file = tempfile.NamedTemporaryFile(
        mode='w+', 
        suffix=extension, 
        dir=temp_dir,
        delete=False
    )
    temp_file.close()
    return temp_file.name

def cleanup_temp_file(file_path: str) -> None:
    """Clean up temporary file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not delete temp file {file_path}: {e}")

def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude coordinates"""
    return -90 <= lat <= 90 and -180 <= lon <= 180

def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate date range format and logic"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except ValueError:
        return False

def format_weather_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format weather data for consistent output"""
    if not data or "main" not in data:
        return {"error": "Invalid weather data"}
    
    # Handle both current weather and forecast data
    if "list" in data:
        # This is forecast data
        formatted_forecast = []
        for item in data.get("list", []):
            formatted_forecast.append({
                "date": item.get("dt_txt", ""),
                "temperature": item.get("main", {}).get("temp", 0),
                "feels_like": item.get("main", {}).get("feels_like", 0),
                "humidity": item.get("main", {}).get("humidity", 0),
                "pressure": item.get("main", {}).get("pressure", 0),
                "weather": item.get("weather", [{}])[0].get("description", "Unknown"),
                "wind_speed": item.get("wind", {}).get("speed", 0),
                "wind_direction": item.get("wind", {}).get("deg", 0),
                "location": data.get("city", {}).get("name", "Unknown")
            })
        return formatted_forecast
    else:
        # This is current weather data
        return {
            "location": data.get("name", "Unknown"),
            "country": data.get("sys", {}).get("country", "Unknown"),
            "temperature": {
                "current": data.get("main", {}).get("temp", 0),
                "feels_like": data.get("main", {}).get("feels_like", 0),
                "min": data.get("main", {}).get("temp_min", 0),
                "max": data.get("main", {}).get("temp_max", 0)
            },
            "humidity": data.get("main", {}).get("humidity", 0),
            "pressure": data.get("main", {}).get("pressure", 0),
            "weather": {
                "main": data.get("weather", [{}])[0].get("main", "Unknown"),
                "description": data.get("weather", [{}])[0].get("description", "Unknown"),
                "icon": data.get("weather", [{}])[0].get("icon", "")
            },
            "wind": {
                "speed": data.get("wind", {}).get("speed", 0),
                "direction": data.get("wind", {}).get("deg", 0)
            },
            "timestamp": datetime.now().isoformat()
        }

def format_stock_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format stock data for consistent output.
    Returns up to 50 most recent entries sorted by date descending.
    """
    if not data or "Time Series (Daily)" not in data:
        return {"error": "Invalid stock data"}

    time_series = data["Time Series (Daily)"]
    formatted_data = []

    for date, values in time_series.items():
        try:
            formatted_data.append({
                "date": date,
                "open": float(values.get("1. open", 0)),
                "high": float(values.get("2. high", 0)),
                "low": float(values.get("3. low", 0)),
                "close": float(values.get("4. close", 0)),
                "volume": int(values.get("5. volume", 0))
            })
        except Exception:
            # Skip malformed rows
            continue

    # Sort by date descending and limit to 50 entries
    try:
        formatted_data.sort(key=lambda x: x["date"], reverse=True)
    except Exception:
        # If dates are not sortable, keep original order
        pass

    limited = formatted_data[:50]

    return {
        "symbol": data.get("Meta Data", {}).get("2. Symbol", "Unknown"),
        "last_refreshed": data.get("Meta Data", {}).get("3. Last Refreshed", ""),
        "data": limited
    }

def format_news_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format news data for consistent output"""
    if not data or "articles" not in data:
        return {"error": "Invalid news data"}
    
    articles = data.get("articles", [])
    formatted_articles = []
    
    for article in articles:
        formatted_articles.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "source": article.get("source", {}).get("name", ""),
            "author": article.get("author", ""),
            "url_to_image": article.get("urlToImage", "")
        })
    
    return {
        "total_results": data.get("totalResults", 0),
        "articles": formatted_articles
    }

def format_image_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format image data for consistent output"""
    if not data or "photos" not in data:
        return {"error": "Invalid image data"}
    
    photos = data.get("photos", [])
    formatted_photos = []
    
    for photo in photos:
        formatted_photos.append({
            "id": photo.get("id", 0),
            "width": photo.get("width", 0),
            "height": photo.get("height", 0),
            "url": photo.get("url", ""),
            "photographer": photo.get("photographer", ""),
            "photographer_url": photo.get("photographer_url", ""),
            "src": {
                "original": photo.get("src", {}).get("original", ""),
                "large": photo.get("src", {}).get("large", ""),
                "medium": photo.get("src", {}).get("medium", ""),
                "small": photo.get("src", {}).get("small", "")
            }
        })
    
    return {
        "total_results": data.get("total_results", 0),
        "photos": formatted_photos
    }

def save_to_csv(data: List[Dict[str, Any]], filename: str) -> str:
    """Save data to CSV file"""
    if not data:
        raise ValueError("No data to save")
    
    file_path = create_temp_file(".csv")
    
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    return file_path

def save_to_json(data: Union[Dict[str, Any], List[Dict[str, Any]]], filename: str) -> str:
    """Save data to JSON file"""
    file_path = create_temp_file(".json")
    
    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    return file_path

def save_to_parquet(data: List[Dict[str, Any]], filename: str) -> str:
    """Save data to Parquet file"""
    if not data:
        raise ValueError("No data to save")
    
    file_path = create_temp_file(".parquet")
    df = pd.DataFrame(data)
    df.to_parquet(file_path, index=False)
    
    return file_path

def download_images(image_urls: List[str], filename: str) -> str:
    """Download images and create ZIP file"""
    if not image_urls:
        raise ValueError("No image URLs provided")
    
    zip_path = create_temp_file(".zip")
    
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for i, url in enumerate(image_urls[:10]):  # Limit to 10 images
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    image_name = f"image_{i+1}.jpg"
                    zip_file.writestr(image_name, response.content)
            except Exception as e:
                print(f"Warning: Could not download image {url}: {e}")
    
    return zip_path

def validate_api_response(response: requests.Response) -> bool:
    """Validate API response"""
    return response.status_code == 200 and response.json() is not None

def handle_api_error(error: Exception, service_name: str) -> Dict[str, Any]:
    """Handle API errors consistently"""
    return {
        "error": f"{service_name} API error",
        "message": str(error),
        "timestamp": datetime.now().isoformat()
    }
