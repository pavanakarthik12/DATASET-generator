# Smart Dataset Generator Backend

A professional, modular backend for generating datasets from multiple APIs using FastAPI and Python. This backend integrates OpenWeatherMap, Alpha Vantage, NewsAPI, Pexels, and OpenRouter chatbot APIs to provide downloadable datasets in various formats.

## 🚀 Features

- **Multi-API Integration**: Weather, stocks, news, images, and COVID-19 data
- **AI-Powered Chatbot**: OpenRouter integration for intelligent suggestions
- **Multiple Export Formats**: CSV, JSON, Parquet, and ZIP downloads
- **Modular Architecture**: Clean, extensible codebase
- **Comprehensive Testing**: Full test suite for all endpoints
- **CORS Support**: Ready for frontend integration

## 📁 Project Structure

```
smart-dataset-generator-backend/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── routes/
│   │   ├── api_routes.py        # Data API endpoints
│   │   ├── chatbot_routes.py    # Chatbot endpoints
│   │   └── download_routes.py   # Download endpoints
│   ├── services/
│   │   ├── openweather_service.py
│   │   ├── alphavantage_service.py
│   │   ├── newsapi_service.py
│   │   ├── pexels_service.py
│   │   └── covid_service.py
│   └── utils/
│       └── helpers.py           # Utility functions
├── config/
│   └── config.py                # Configuration management
├── tests/
│   └── test_all_apis.py         # Comprehensive test suite
├── data/                        # Temporary file storage
├── env.example                  # Environment variables template
├── requirements.txt
└── README.md
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-dataset-generator-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

## 🔑 API Keys Setup

Get your free API keys from these services:

- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key
- **NewsAPI**: https://newsapi.org/register
- **OpenWeatherMap**: https://openweathermap.org/api
- **Pexels**: https://www.pexels.com/api/
- **OpenRouter**: https://openrouter.ai/

Add them to your `.env` file:
```env
ALPHAVANTAGE_API_KEY=your_key_here
NEWSAPI_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
PEXELS_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

## 🚀 Running the Application

1. **Start the server**
   ```bash
   python app/main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## 📊 API Endpoints

### Data APIs (`/api`)

#### Weather
- `GET /api/weather/current?city=London` - Current weather
- `GET /api/weather/coordinates?lat=51.5&lon=-0.1` - Weather by coordinates
- `GET /api/weather/forecast?city=NewYork&days=5` - Weather forecast

#### Stocks
- `GET /api/stocks/quote/{symbol}` - Stock quote
- `GET /api/stocks/daily/{symbol}` - Daily stock data
- `GET /api/stocks/company/{symbol}` - Company overview

#### News
- `GET /api/news/headlines?country=us` - Top headlines
- `GET /api/news/search?query=technology` - Search news
- `GET /api/news/trending?country=us` - Trending topics

#### Images
- `GET /api/images/search?query=nature` - Search images
- `GET /api/images/curated` - Curated images
- `GET /api/images/category/{category}` - Images by category

#### COVID-19
- `GET /api/covid/global` - Global COVID data
- `GET /api/covid/country/{country}` - Country COVID data
- `GET /api/covid/top-countries` - Top countries by cases

### Chatbot APIs (`/chatbot`)

- `POST /chatbot/suggest?query=How to analyze weather data?` - AI suggestions
- `POST /chatbot/recommendations?data_type=weather&purpose=analysis` - Dataset recommendations
- `POST /chatbot/analyze?data_sample=...` - Data quality analysis

### Download APIs (`/download`)

- `GET /download/weather/csv?city=London` - Weather CSV
- `GET /download/weather/json?city=Paris` - Weather JSON
- `GET /download/stocks/csv/{symbol}` - Stock CSV
- `GET /download/stocks/parquet/{symbol}` - Stock Parquet
- `GET /download/news/csv?query=technology` - News CSV
- `GET /download/news/json?query=science` - News JSON
- `GET /download/images/zip?query=nature` - Image ZIP
- `GET /download/covid/csv/{country}` - COVID CSV
- `GET /download/combined/csv` - Combined data CSV

## 🧪 Testing

Run the comprehensive test suite:

```bash
python tests/test_all_apis.py
```

The test suite will:
- Test all API endpoints
- Verify data formats
- Check download functionality
- Generate a detailed report

## 📁 Data Storage

- Temporary files are stored in `data/temp/`
- Files are automatically cleaned up after download
- Ensure the `data/` directory exists and is writable

## 🔧 Configuration

The application uses environment variables for configuration:

- API keys are loaded from `.env` file
- CORS is configured for frontend integration
- Rate limiting can be adjusted in `config/config.py`
- File storage paths are configurable

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use proper secret management
2. **CORS**: Configure allowed origins for production
3. **Rate Limiting**: Implement proper rate limiting
4. **File Cleanup**: Set up automated cleanup for temp files
5. **Monitoring**: Add logging and monitoring
6. **Security**: Implement authentication if needed

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Run the test suite to verify setup
3. Check environment variables configuration
4. Review error logs for specific issues

## 🔄 Updates

- **v1.0.0**: Initial release with all core features
- Modular architecture for easy extension
- Comprehensive test coverage
- Production-ready configuration
