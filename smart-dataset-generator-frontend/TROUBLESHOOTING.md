# Troubleshooting Guide

## Common Backend Errors and Solutions

### 1. 500 Internal Server Errors

The 500 errors you're seeing are typically caused by:

#### **API Key Issues**
- **Problem**: Missing or invalid API keys for external services
- **Solution**: Check that all required API keys are configured in the backend:
  - OpenWeatherMap API key
  - Alpha Vantage API key  
  - NewsAPI key
  - Pexels API key
  - OpenRouter API key

#### **Invalid Parameters**
- **Problem**: Frontend sending invalid parameters (like "weather" as city name)
- **Solution**: The frontend now includes proper validation to prevent this

#### **Service Dependencies**
- **Problem**: External API services are down or rate-limited
- **Solution**: Check service status and implement retry logic

### 2. Frontend Error Handling Improvements

The frontend now includes:

#### **Enhanced Validation**
- City names must be at least 2 characters
- Stock symbols must be 1-10 characters, letters and numbers only
- Coordinates must be valid numbers within proper ranges
- Page sizes must be within valid limits

#### **Better Error Messages**
- Specific error messages for different validation failures
- Network error handling with retry suggestions
- Backend status indicator

#### **Improved API Integration**
- Response interceptors for consistent error handling
- Timeout handling for slow responses
- Proper error propagation from backend

### 3. Backend Configuration Issues

#### **Check Backend Health**
```bash
curl http://localhost:8000/health
```

#### **Verify API Keys**
Check the backend configuration file for all required API keys:
- `OPENWEATHER_API_KEY`
- `ALPHA_VANTAGE_API_KEY`
- `NEWSAPI_API_KEY`
- `PEXELS_API_KEY`
- `OPENROUTER_API_KEY`

#### **Check Backend Logs**
Look for specific error messages in the backend console output.

### 4. Common Solutions

#### **For Weather API Errors**
- Ensure city names are real cities
- Check if OpenWeatherMap API key is valid
- Verify API quota hasn't been exceeded

#### **For Stock API Errors**
- Use valid stock symbols (e.g., AAPL, MSFT, GOOGL)
- Check Alpha Vantage API key and quota
- Some symbols may not be available

#### **For News API Errors**
- Use valid country codes (us, gb, ca, etc.)
- Check NewsAPI key and quota
- Some categories may not be available for all countries

#### **For Image API Errors**
- Use descriptive search terms
- Check Pexels API key and quota
- Some categories may not have images

### 5. Frontend Error Prevention

The updated frontend now:

1. **Validates all inputs** before sending to backend
2. **Shows specific error messages** for different failure types
3. **Includes a backend status indicator** to show connection health
4. **Handles network errors** gracefully
5. **Prevents invalid parameter combinations**

### 6. Testing the Fixes

1. **Start the backend** and verify it's running on port 8000
2. **Check the backend status indicator** in the top-right corner
3. **Try valid inputs** first (e.g., "London" for weather, "AAPL" for stocks)
4. **Test error handling** with invalid inputs
5. **Verify downloads work** with valid data

### 7. Backend Service Dependencies

Make sure these external services are accessible:
- OpenWeatherMap API
- Alpha Vantage API
- NewsAPI
- Pexels API
- OpenRouter API

If any service is down, the corresponding endpoints will return 500 errors.

### 8. Rate Limiting

Some APIs have rate limits. If you hit them:
- Wait before making more requests
- Consider implementing request queuing
- Check API documentation for rate limits

The frontend now includes better error handling and validation to prevent most common issues that cause 500 errors.
