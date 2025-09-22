"""
Comprehensive test suite for Smart Dataset Generator API
Tests all APIs and chatbot functionality
"""

import requests
import json
import time
from typing import Dict, Any

class APITester:
    """Test suite for all API endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
    
    def test_endpoint(self, method: str, endpoint: str, params: Dict[str, Any] = None, 
                     data: Dict[str, Any] = None, expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, params=params, timeout=10)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": response.status_code == expected_status,
                "response_time": response.elapsed.total_seconds(),
                "timestamp": time.time()
            }
            
            try:
                result["response_data"] = response.json()
            except:
                result["response_data"] = response.text[:500]  # Limit text response
            
            if response.status_code != expected_status:
                result["error"] = f"Expected status {expected_status}, got {response.status_code}"
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                "endpoint": endpoint,
                "method": method,
                "error": str(e),
                "success": False,
                "timestamp": time.time()
            }
    
    def test_weather_apis(self):
        """Test weather API endpoints"""
        print("Testing Weather APIs...")
        
        # Test current weather
        result = self.test_endpoint("GET", "/api/weather/current", {"city": "London"})
        self.results.append(result)
        print(f"✓ Current Weather: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test weather by coordinates
        result = self.test_endpoint("GET", "/api/weather/coordinates", {"lat": 51.5074, "lon": -0.1278})
        self.results.append(result)
        print(f"✓ Weather by Coordinates: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test weather forecast
        result = self.test_endpoint("GET", "/api/weather/forecast", {"city": "New York", "days": 3})
        self.results.append(result)
        print(f"✓ Weather Forecast: {'PASS' if result['success'] else 'FAIL'}")
    
    def test_stock_apis(self):
        """Test stock market API endpoints"""
        print("\nTesting Stock Market APIs...")
        
        # Test stock quote
        result = self.test_endpoint("GET", "/api/stocks/quote/AAPL")
        self.results.append(result)
        print(f"✓ Stock Quote: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test daily stock data
        result = self.test_endpoint("GET", "/api/stocks/daily/MSFT", {"outputsize": "compact"})
        self.results.append(result)
        print(f"✓ Daily Stock Data: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test company overview
        result = self.test_endpoint("GET", "/api/stocks/company/GOOGL")
        self.results.append(result)
        print(f"✓ Company Overview: {'PASS' if result['success'] else 'FAIL'}")
    
    def test_news_apis(self):
        """Test news API endpoints"""
        print("\nTesting News APIs...")
        
        # Test top headlines
        result = self.test_endpoint("GET", "/api/news/headlines", {"country": "us", "page_size": 10})
        self.results.append(result)
        print(f"✓ Top Headlines: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test news search
        result = self.test_endpoint("GET", "/api/news/search", {"query": "technology", "page_size": 10})
        self.results.append(result)
        print(f"✓ News Search: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test trending topics
        result = self.test_endpoint("GET", "/api/news/trending", {"country": "us", "category": "technology"})
        self.results.append(result)
        print(f"✓ Trending Topics: {'PASS' if result['success'] else 'FAIL'}")
    
    def test_image_apis(self):
        """Test image API endpoints"""
        print("\nTesting Image APIs...")
        
        # Test image search
        result = self.test_endpoint("GET", "/api/images/search", {"query": "nature", "per_page": 10})
        self.results.append(result)
        print(f"✓ Image Search: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test curated images
        result = self.test_endpoint("GET", "/api/images/curated", {"per_page": 10})
        self.results.append(result)
        print(f"✓ Curated Images: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test images by category
        result = self.test_endpoint("GET", "/api/images/category/business", {"per_page": 10})
        self.results.append(result)
        print(f"✓ Images by Category: {'PASS' if result['success'] else 'FAIL'}")
    
    def test_covid_apis(self):
        """Test COVID-19 API endpoints"""
        print("\nTesting COVID-19 APIs...")
        
        # Test global COVID data
        result = self.test_endpoint("GET", "/api/covid/global")
        self.results.append(result)
        print(f"✓ Global COVID Data: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test country COVID data
        result = self.test_endpoint("GET", "/api/covid/country/US")
        self.results.append(result)
        print(f"✓ Country COVID Data: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test top countries
        result = self.test_endpoint("GET", "/api/covid/top-countries", {"limit": 5})
        self.results.append(result)
        print(f"✓ Top Countries: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test available countries
        result = self.test_endpoint("GET", "/api/covid/countries")
        self.results.append(result)
        print(f"✓ Available Countries: {'PASS' if result['success'] else 'FAIL'}")
    
    def test_chatbot_apis(self):
        """Test chatbot API endpoints"""
        print("\nTesting Chatbot APIs...")
        
        # Test suggestion endpoint
        result = self.test_endpoint("POST", "/chatbot/suggest", {"query": "How to analyze weather data?"})
        self.results.append(result)
        print(f"✓ Chatbot Suggestion: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test recommendations endpoint
        result = self.test_endpoint("POST", "/chatbot/recommendations", 
                                  {"data_type": "weather", "purpose": "climate analysis"})
        self.results.append(result)
        print(f"✓ Dataset Recommendations: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test data analysis endpoint
        result = self.test_endpoint("POST", "/chatbot/analyze", 
                                  {"data_sample": "Temperature: 25°C, Humidity: 60%, Pressure: 1013 hPa"})
        self.results.append(result)
        print(f"✓ Data Quality Analysis: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test models endpoint
        result = self.test_endpoint("GET", "/chatbot/models")
        self.results.append(result)
        print(f"✓ Available Models: {'PASS' if result['success'] else 'FAIL'}")
    
    def test_download_apis(self):
        """Test download API endpoints"""
        print("\nTesting Download APIs...")
        
        # Test weather CSV download
        result = self.test_endpoint("GET", "/download/weather/csv", {"city": "London"})
        self.results.append(result)
        print(f"✓ Weather CSV Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test weather JSON download
        result = self.test_endpoint("GET", "/download/weather/json", {"city": "Paris"})
        self.results.append(result)
        print(f"✓ Weather JSON Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test stock CSV download
        result = self.test_endpoint("GET", "/download/stocks/csv/AAPL")
        self.results.append(result)
        print(f"✓ Stock CSV Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test stock Parquet download
        result = self.test_endpoint("GET", "/download/stocks/parquet/MSFT")
        self.results.append(result)
        print(f"✓ Stock Parquet Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test news CSV download
        result = self.test_endpoint("GET", "/download/news/csv", {"query": "technology", "page_size": 10})
        self.results.append(result)
        print(f"✓ News CSV Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test news JSON download
        result = self.test_endpoint("GET", "/download/news/json", {"query": "science", "page_size": 10})
        self.results.append(result)
        print(f"✓ News JSON Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test image ZIP download
        result = self.test_endpoint("GET", "/download/images/zip", {"query": "nature", "per_page": 5})
        self.results.append(result)
        print(f"✓ Image ZIP Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test COVID CSV download
        result = self.test_endpoint("GET", "/download/covid/csv/US")
        self.results.append(result)
        print(f"✓ COVID CSV Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test COVID JSON download
        result = self.test_endpoint("GET", "/download/covid/json/UK")
        self.results.append(result)
        print(f"✓ COVID JSON Download: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test combined CSV download
        result = self.test_endpoint("GET", "/download/combined/csv", 
                                  {"weather_city": "Tokyo", "stock_symbol": "AAPL", "news_query": "AI"})
        self.results.append(result)
        print(f"✓ Combined CSV Download: {'PASS' if result['success'] else 'FAIL'}")
    
    def test_basic_endpoints(self):
        """Test basic API endpoints"""
        print("\nTesting Basic Endpoints...")
        
        # Test root endpoint
        result = self.test_endpoint("GET", "/")
        self.results.append(result)
        print(f"✓ Root Endpoint: {'PASS' if result['success'] else 'FAIL'}")
        
        # Test health check
        result = self.test_endpoint("GET", "/health")
        self.results.append(result)
        print(f"✓ Health Check: {'PASS' if result['success'] else 'FAIL'}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("SMART DATASET GENERATOR API TEST SUITE")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test categories
        self.test_basic_endpoints()
        self.test_weather_apis()
        self.test_stock_apis()
        self.test_news_apis()
        self.test_image_apis()
        self.test_covid_apis()
        self.test_chatbot_apis()
        self.test_download_apis()
        
        end_time = time.time()
        
        # Generate summary
        self.generate_summary(end_time - start_time)
    
    def generate_summary(self, total_time: float):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result.get("success", False))
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Total Time: {total_time:.2f} seconds")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.results:
                if not result.get("success", False):
                    print(f"✗ {result.get('method', 'GET')} {result.get('endpoint', 'Unknown')}")
                    if "error" in result:
                        print(f"  Error: {result['error']}")
        
        print("\n" + "=" * 60)
        print("Test completed!")

def main():
    """Main test function"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
