import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || 
                          error.response.data?.error || 
                          `Server error: ${error.response.status}`;
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error: Unable to connect to server');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

// Weather API functions
export const weatherAPI = {
  getCurrentWeather: async (city, countryCode = null) => {
    try {
      const params = { city };
      if (countryCode) params.country_code = countryCode;
      
      const response = await api.get('/api/weather/current', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch weather data');
    }
  },

  getWeatherByCoordinates: async (lat, lon) => {
    try {
      const response = await api.get('/api/weather/coordinates', {
        params: { lat, lon }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch weather data');
    }
  },

  getWeatherForecast: async (city, days = 5) => {
    try {
      const response = await api.get('/api/weather/forecast', {
        params: { city, days }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch weather forecast');
    }
  }
};

// Stocks API functions
export const stocksAPI = {
  getStockQuote: async (symbol) => {
    try {
      const response = await api.get(`/api/stocks/quote/${symbol}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch stock quote');
    }
  },

  getDailyStockData: async (symbol, outputsize = 'compact') => {
    try {
      const response = await api.get(`/api/stocks/daily/${symbol}`, {
        params: { outputsize }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch stock data');
    }
  },

  getCompanyOverview: async (symbol) => {
    try {
      const response = await api.get(`/api/stocks/company/${symbol}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch company overview');
    }
  }
};

// News API functions
export const newsAPI = {
  getTopHeadlines: async (country = 'us', category = null, pageSize = 20) => {
    try {
      const params = { country, page_size: pageSize };
      if (category) params.category = category;
      
      const response = await api.get('/api/news/headlines', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch news headlines');
    }
  },

  searchNews: async (query, language = 'en', pageSize = 20) => {
    try {
      const response = await api.get('/api/news/search', {
        params: { query, language, page_size: pageSize }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to search news');
    }
  },

  getTrendingTopics: async (country = 'us', category = 'general') => {
    try {
      const response = await api.get('/api/news/trending', {
        params: { country, category }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch trending topics');
    }
  }
};

// Images API functions
export const imagesAPI = {
  searchImages: async (query, perPage = 15, orientation = null, color = null) => {
    try {
      const params = { query, per_page: perPage };
      if (orientation) params.orientation = orientation;
      if (color) params.color = color;
      
      const response = await api.get('/api/images/search', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to search images');
    }
  },

  getCuratedImages: async (perPage = 15) => {
    try {
      const response = await api.get('/api/images/curated', {
        params: { per_page: perPage }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch curated images');
    }
  },

  getImagesByCategory: async (category, perPage = 15) => {
    try {
      const response = await api.get(`/api/images/category/${category}`, {
        params: { per_page: perPage }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch images by category');
    }
  }
};

// COVID-19 API functions
export const covidAPI = {
  getGlobalData: async () => {
    try {
      const response = await api.get('/api/covid/global');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch global COVID data');
    }
  },

  getCountryData: async (country) => {
    try {
      const response = await api.get(`/api/covid/country/${country}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch country COVID data');
    }
  },

  getTopCountries: async (limit = 10) => {
    try {
      const response = await api.get('/api/covid/top-countries', {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch top countries data');
    }
  },

  getAvailableCountries: async () => {
    try {
      const response = await api.get('/api/covid/countries');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch available countries');
    }
  }
};

// Chatbot API functions
export const chatbotAPI = {
  getSuggestion: async (query, context = null) => {
    try {
      const params = { query };
      if (context) params.context = context;
      
      const response = await api.post('/chatbot/suggest', null, { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get AI suggestion');
    }
  },

  getRecommendations: async (dataType, purpose) => {
    try {
      const response = await api.post('/chatbot/recommendations', null, {
        params: { data_type: dataType, purpose }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get recommendations');
    }
  },

  analyzeDataQuality: async (dataSample) => {
    try {
      const response = await api.post('/chatbot/analyze', null, {
        params: { data_sample: dataSample }
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to analyze data quality');
    }
  }
};

// Download API functions
export const downloadAPI = {
  downloadWeatherCSV: async (city, countryCode = null) => {
    try {
      const params = { city };
      if (countryCode) params.country_code = countryCode;
      
      const response = await api.get('/download/weather/csv', { 
        params,
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download weather CSV');
    }
  },

  downloadWeatherJSON: async (city, countryCode = null) => {
    try {
      const params = { city };
      if (countryCode) params.country_code = countryCode;
      
      const response = await api.get('/download/weather/json', { 
        params,
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download weather JSON');
    }
  },

  downloadStocksCSV: async (symbol, outputsize = 'compact') => {
    try {
      const response = await api.get(`/download/stocks/csv/${symbol}`, { 
        params: { outputsize },
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download stocks CSV');
    }
  },

  downloadStocksParquet: async (symbol, outputsize = 'compact') => {
    try {
      const response = await api.get(`/download/stocks/parquet/${symbol}`, { 
        params: { outputsize },
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download stocks Parquet');
    }
  },

  downloadNewsCSV: async (query, language = 'en', pageSize = 20) => {
    try {
      const response = await api.get('/download/news/csv', { 
        params: { query, language, page_size: pageSize },
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download news CSV');
    }
  },

  downloadNewsJSON: async (query, language = 'en', pageSize = 20) => {
    try {
      const response = await api.get('/download/news/json', { 
        params: { query, language, page_size: pageSize },
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download news JSON');
    }
  },

  downloadImagesZIP: async (query, perPage = 10, orientation = null) => {
    try {
      const params = { query, per_page: perPage };
      if (orientation) params.orientation = orientation;
      
      const response = await api.get('/download/images/zip', { 
        params,
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download images ZIP');
    }
  },

  downloadCovidCSV: async (country) => {
    try {
      const response = await api.get(`/download/covid/csv/${country}`, { 
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download COVID CSV');
    }
  },

  downloadCovidJSON: async (country) => {
    try {
      const response = await api.get(`/download/covid/json/${country}`, { 
        responseType: 'blob'
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to download COVID JSON');
    }
  }
};

// Utility function to trigger file download
export const downloadFile = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};
