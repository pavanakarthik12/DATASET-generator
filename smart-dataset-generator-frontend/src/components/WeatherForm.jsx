import React, { useState } from 'react';
import { weatherAPI } from '../api/api';

const WeatherForm = ({ onDataUpdate, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    city: '',
    countryCode: '',
    lat: '',
    lon: '',
    days: 5
  });
  const [searchType, setSearchType] = useState('city');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    onLoading(true);
    onError(null);

    try {
      let response;
      let weatherDataArray = [];
      
      if (searchType === 'city') {
        if (!formData.city.trim()) {
          throw new Error('City name is required');
        }
        if (formData.city.trim().length < 2) {
          throw new Error('City name must be at least 2 characters');
        }
        
        // Get 5-day forecast to get more data points (up to ~40 entries)
        const forecastResponse = await weatherAPI.getWeatherForecast(formData.city.trim(), 5);
        if (forecastResponse.success && forecastResponse.data) {
          // Extract forecast data points
          if (forecastResponse.data.list && Array.isArray(forecastResponse.data.list)) {
            weatherDataArray = forecastResponse.data.list.slice(0, 50).map((item) => ({
              date: (item.dt_txt || new Date(item.dt * 1000).toISOString()),
              temperature: item.main?.temp || 0,
              feels_like: item.main?.feels_like || 0,
              humidity: item.main?.humidity || 0,
              pressure: item.main?.pressure || 0,
              weather: item.weather?.[0]?.description || 'Unknown',
              wind_speed: item.wind?.speed || 0,
              wind_direction: item.wind?.deg || 0,
              location: formData.city.trim()
            }));
          }
        }
        
        // Fallback to current weather as single-entry array if no forecast data
        if (weatherDataArray.length === 0) {
          const currentResponse = await weatherAPI.getCurrentWeather(formData.city.trim(), formData.countryCode || null);
          if (currentResponse.success && currentResponse.data) {
            const cur = currentResponse.data;
            weatherDataArray = [{
              date: cur.timestamp || new Date().toISOString(),
              temperature: cur.temperature?.current || 0,
              feels_like: cur.temperature?.feels_like || 0,
              humidity: cur.humidity || 0,
              pressure: cur.pressure || 0,
              weather: cur.weather?.description || cur.weather || 'Unknown',
              wind_speed: cur.wind?.speed || 0,
              wind_direction: cur.wind?.direction || 0,
              location: cur.location || formData.city.trim()
            }];
          }
        }
        
        response = { success: true, data: weatherDataArray };
      } else if (searchType === 'coordinates') {
        if (!formData.lat || !formData.lon) {
          throw new Error('Both latitude and longitude are required');
        }
        const lat = parseFloat(formData.lat);
        const lon = parseFloat(formData.lon);
        if (isNaN(lat) || isNaN(lon)) {
          throw new Error('Latitude and longitude must be valid numbers');
        }
        if (lat < -90 || lat > 90) {
          throw new Error('Latitude must be between -90 and 90');
        }
        if (lon < -180 || lon > 180) {
          throw new Error('Longitude must be between -180 and 180');
        }
        
        // Try forecast by city is not available for pure coords; use current as single-entry array
        const currentResponse = await weatherAPI.getWeatherByCoordinates(lat, lon);
        if (currentResponse.success && currentResponse.data) {
          const cur = currentResponse.data;
          weatherDataArray = [{
            date: cur.timestamp || new Date().toISOString(),
            temperature: cur.temperature?.current || 0,
            feels_like: cur.temperature?.feels_like || 0,
            humidity: cur.humidity || 0,
            pressure: cur.pressure || 0,
            weather: cur.weather?.description || cur.weather || 'Unknown',
            wind_speed: cur.wind?.speed || 0,
            wind_direction: cur.wind?.direction || 0,
            location: cur.location || `${lat},${lon}`
          }];
        }
        
        response = { success: true, data: weatherDataArray };
      } else if (searchType === 'forecast') {
        if (!formData.city.trim()) {
          throw new Error('City name is required for forecast');
        }
        if (formData.city.trim().length < 2) {
          throw new Error('City name must be at least 2 characters');
        }
        const days = parseInt(formData.days);
        if (isNaN(days) || days < 1 || days > 5) {
          throw new Error('Days must be a number between 1 and 5');
        }
        
        const forecastResponse = await weatherAPI.getWeatherForecast(formData.city.trim(), days);
        if (forecastResponse.success && forecastResponse.data) {
          // Extract forecast data points
          if (forecastResponse.data.list && Array.isArray(forecastResponse.data.list)) {
            const maxEntries = Math.min(days * 8, 50);
            weatherDataArray = forecastResponse.data.list.slice(0, maxEntries).map((item) => ({
              date: (item.dt_txt || new Date(item.dt * 1000).toISOString()),
              temperature: item.main?.temp || 0,
              feels_like: item.main?.feels_like || 0,
              humidity: item.main?.humidity || 0,
              pressure: item.main?.pressure || 0,
              weather: item.weather?.[0]?.description || 'Unknown',
              wind_speed: item.wind?.speed || 0,
              wind_direction: item.wind?.deg || 0,
              location: formData.city.trim()
            }));
          }
        }
        
        response = { success: true, data: weatherDataArray };
      }

      if (response.success && response.data && response.data.length > 0) {
        const params = {
          city: formData.city.trim(),
          countryCode: formData.countryCode || null,
          lat: formData.lat,
          lon: formData.lon,
          days: formData.days
        };
        onDataUpdate(response.data, 'weather', params);
      } else {
        throw new Error('No weather data available');
      }
    } catch (error) {
      onError(error.message);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="form-card" id="weather">
      <h3>Weather Data</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Search Type:</label>
          <select 
            value={searchType} 
            onChange={(e) => setSearchType(e.target.value)}
          >
            <option value="city">Current Weather by City</option>
            <option value="coordinates">Weather by Coordinates</option>
            <option value="forecast">Weather Forecast</option>
          </select>
        </div>

        {searchType === 'city' && (
          <>
            <div className="form-group">
              <label htmlFor="city">City Name:</label>
              <input
                type="text"
                id="city"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                placeholder="e.g., London, New York"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="countryCode">Country Code (Optional):</label>
              <input
                type="text"
                id="countryCode"
                name="countryCode"
                value={formData.countryCode}
                onChange={handleInputChange}
                placeholder="e.g., US, GB, CA"
                maxLength="2"
              />
            </div>
          </>
        )}

        {searchType === 'coordinates' && (
          <>
            <div className="form-group">
              <label htmlFor="lat">Latitude:</label>
              <input
                type="number"
                id="lat"
                name="lat"
                value={formData.lat}
                onChange={handleInputChange}
                placeholder="e.g., 40.7128"
                step="any"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="lon">Longitude:</label>
              <input
                type="number"
                id="lon"
                name="lon"
                value={formData.lon}
                onChange={handleInputChange}
                placeholder="e.g., -74.0060"
                step="any"
                required
              />
            </div>
          </>
        )}

        {searchType === 'forecast' && (
          <>
            <div className="form-group">
              <label htmlFor="city">City Name:</label>
              <input
                type="text"
                id="city"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                placeholder="e.g., London, New York"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="days">Forecast Days (1-5):</label>
              <input
                type="number"
                id="days"
                name="days"
                value={formData.days}
                onChange={handleInputChange}
                min="1"
                max="5"
                required
              />
            </div>
          </>
        )}

        <button type="submit" className="form-button">
          Get Weather Data
        </button>
      </form>
    </div>
  );
};

export default WeatherForm;
