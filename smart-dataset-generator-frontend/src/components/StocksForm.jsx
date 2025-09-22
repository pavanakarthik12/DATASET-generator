import React, { useState } from 'react';
import { stocksAPI } from '../api/api';

const StocksForm = ({ onDataUpdate, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    symbol: '',
    outputsize: 'compact'
  });
  const [searchType, setSearchType] = useState('quote');

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
      let symbol = '';
      
      if (searchType !== 'multiple') {
        if (!formData.symbol.trim()) {
          throw new Error('Stock symbol is required');
        }
        
        symbol = formData.symbol.trim().toUpperCase();
        if (symbol.length < 1 || symbol.length > 10) {
          throw new Error('Stock symbol must be 1-10 characters');
        }
        
        // Basic validation for stock symbols (letters and numbers only)
        if (!/^[A-Z0-9]+$/.test(symbol)) {
          throw new Error('Stock symbol can only contain letters and numbers');
        }
      } else if (formData.symbol.trim()) {
        // Optional validation for multiple stocks
        symbol = formData.symbol.trim().toUpperCase();
        if (symbol.length < 1 || symbol.length > 10) {
          throw new Error('Stock symbol must be 1-10 characters');
        }
        
        if (!/^[A-Z0-9]+$/.test(symbol)) {
          throw new Error('Stock symbol can only contain letters and numbers');
        }
      }

      let response;
      let stockDataArray = [];
      
      if (searchType === 'quote') {
        response = await stocksAPI.getStockQuote(symbol);
        if (response.success && response.data) {
          stockDataArray.push(response.data);
        }
      } else if (searchType === 'daily') {
        response = await stocksAPI.getDailyStockData(symbol, formData.outputsize);
        if (response.success && response.data) {
          // Extract time series data
          if (response.data.data && Array.isArray(response.data.data)) {
            // Use formatted data from backend
            stockDataArray = response.data.data.slice(0, 50); // Limit to 50 entries
          } else if (response.data['Time Series (Daily)']) {
            // Handle raw time series data
            const timeSeries = response.data['Time Series (Daily)'];
            const dates = Object.keys(timeSeries).slice(0, 50); // Limit to 50 entries
            
            dates.forEach(date => {
              const dayData = timeSeries[date];
              stockDataArray.push({
                date: date,
                open: parseFloat(dayData['1. open']),
                high: parseFloat(dayData['2. high']),
                low: parseFloat(dayData['3. low']),
                close: parseFloat(dayData['4. close']),
                volume: parseInt(dayData['5. volume']),
                symbol: symbol
              });
            });
          }
        }
      } else if (searchType === 'company') {
        response = await stocksAPI.getCompanyOverview(symbol);
        if (response.success && response.data) {
          stockDataArray.push(response.data);
        }
      } else if (searchType === 'multiple') {
        // Fetch multiple popular stocks for comparison
        const popularStocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX'];
        let stocksToFetch = popularStocks.slice(0, 5); // Limit to 5 stocks
        
        // If user provided a symbol, include it and reduce popular stocks
        if (symbol) {
          stocksToFetch = [symbol, ...popularStocks.filter(s => s !== symbol)].slice(0, 5);
        }
        
        for (const stockSymbol of stocksToFetch) {
          try {
            const stockResponse = await stocksAPI.getStockQuote(stockSymbol);
            if (stockResponse.success && stockResponse.data) {
              stockDataArray.push({
                ...stockResponse.data,
                symbol: stockSymbol
              });
            }
          } catch (error) {
            console.warn(`Failed to fetch data for ${stockSymbol}:`, error.message);
          }
        }
      }

      if (stockDataArray.length > 0) {
        const params = {
          symbol: symbol,
          outputsize: formData.outputsize
        };
        onDataUpdate(stockDataArray, 'stocks', params);
      } else {
        throw new Error('No stock data available');
      }
    } catch (error) {
      onError(error.message);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="form-card" id="stocks">
      <h3 className="form-title">
        <svg className="form-title-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
        Stock Market Data
      </h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Data Type:</label>
          <select 
            value={searchType} 
            onChange={(e) => setSearchType(e.target.value)}
          >
            <option value="quote">Real-time Quote</option>
            <option value="daily">Daily Data</option>
            <option value="company">Company Overview</option>
            <option value="multiple">Multiple Stocks Comparison</option>
          </select>
        </div>

        {searchType !== 'multiple' && (
          <div className="form-group">
            <label htmlFor="symbol">Stock Symbol:</label>
            <input
              type="text"
              id="symbol"
              name="symbol"
              value={formData.symbol}
              onChange={handleInputChange}
              placeholder="e.g., AAPL, MSFT, GOOGL"
              required
            />
          </div>
        )}

        {searchType === 'multiple' && (
          <div className="form-group">
            <label htmlFor="symbol">Stock Symbol (Optional - for additional stock):</label>
            <input
              type="text"
              id="symbol"
              name="symbol"
              value={formData.symbol}
              onChange={handleInputChange}
              placeholder="e.g., AAPL (will fetch AAPL + 4 other popular stocks)"
            />
          </div>
        )}

        {searchType === 'daily' && (
          <div className="form-group">
            <label htmlFor="outputsize">Output Size:</label>
            <select
              id="outputsize"
              name="outputsize"
              value={formData.outputsize}
              onChange={handleInputChange}
            >
              <option value="compact">Compact (100 data points)</option>
              <option value="full">Full (20+ years of data)</option>
            </select>
          </div>
        )}

        <button type="submit" className="btn btn-primary btn-stocks">
          Get Stock Data
        </button>
      </form>
    </div>
  );
};

export default StocksForm;
