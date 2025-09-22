# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your API keys
# Get free keys from:
# - Alpha Vantage: https://www.alphavantage.co/support/#api-key
# - NewsAPI: https://newsapi.org/register
# - OpenWeatherMap: https://openweathermap.org/api
# - Pexels: https://www.pexels.com/api/
# - OpenRouter: https://openrouter.ai/
```

### 3. Test Your Setup
```bash
python test_setup.py
```

### 4. Start the Server
```bash
python start.py
```

### 5. Access Your API
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🧪 Run Tests
```bash
python tests/test_all_apis.py
```

## 📊 Example API Calls

### Get Weather Data
```bash
curl "http://localhost:8000/api/weather/current?city=London"
```

### Get Stock Data
```bash
curl "http://localhost:8000/api/stocks/quote/AAPL"
```

### Download Weather CSV
```bash
curl "http://localhost:8000/download/weather/csv?city=Paris" -o weather.csv
```

### Get AI Suggestion
```bash
curl -X POST "http://localhost:8000/chatbot/suggest?query=How to analyze weather data?"
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the project directory
2. **API Key Errors**: Check your .env file has valid keys
3. **Port Already in Use**: Change port in start.py or kill existing process
4. **Permission Errors**: Ensure data/ directory is writable

### Getting Help

1. Check the full README.md for detailed documentation
2. Run `python test_setup.py` to diagnose issues
3. Check the API documentation at /docs when server is running
