import React from 'react';

const DatasetTable = ({ data, dataType }) => {
  const renderTableContent = () => {
    if (!data) return null;

    switch (dataType) {
      case 'weather':
        return renderWeatherData(data);
      case 'stocks':
        return renderStocksData(data);
      case 'news':
        return renderNewsData(data);
      case 'images':
        return renderImagesData(data);
      default:
        return renderGenericData(data);
    }
  };

  const renderWeatherData = (data) => {
    // Handle array of weather data points
    if (Array.isArray(data) && data.length > 0) {
      return (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Temperature</th>
              <th>Feels Like</th>
              <th>Humidity</th>
              <th>Weather</th>
              <th>Wind Speed</th>
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 50).map((item, index) => (
              <tr key={index}>
                <td>{item.date || item.timestamp || 'N/A'}</td>
                <td>{item.temperature || item.temp_c || 'N/A'}°C</td>
                <td>{item.feels_like || 'N/A'}°C</td>
                <td>{item.humidity || 'N/A'}%</td>
                <td>{item.weather || item.description || 'N/A'}</td>
                <td>{item.wind_speed || item.wind_kph || 'N/A'} km/h</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (data.current) {
      // Current weather data
      return (
        <table>
          <thead>
            <tr>
              <th>Property</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Location</td><td>{data.location?.name}, {data.location?.country}</td></tr>
            <tr><td>Temperature</td><td>{data.current?.temp_c}°C ({data.current?.temp_f}°F)</td></tr>
            <tr><td>Condition</td><td>{data.current?.condition?.text}</td></tr>
            <tr><td>Humidity</td><td>{data.current?.humidity}%</td></tr>
            <tr><td>Wind Speed</td><td>{data.current?.wind_kph} km/h</td></tr>
            <tr><td>Pressure</td><td>{data.current?.pressure_mb} mb</td></tr>
            <tr><td>UV Index</td><td>{data.current?.uv}</td></tr>
            <tr><td>Last Updated</td><td>{data.current?.last_updated}</td></tr>
          </tbody>
        </table>
      );
    } else if (data.forecast) {
      // Forecast data
      return (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Max Temp</th>
              <th>Min Temp</th>
              <th>Condition</th>
              <th>Chance of Rain</th>
            </tr>
          </thead>
          <tbody>
            {data.forecast.forecastday?.map((day, index) => (
              <tr key={index}>
                <td>{day.date}</td>
                <td>{day.day?.maxtemp_c}°C</td>
                <td>{day.day?.mintemp_c}°C</td>
                <td>{day.day?.condition?.text}</td>
                <td>{day.day?.chance_of_rain}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (data.data && Array.isArray(data.data)) {
      // Formatted weather data from backend
      return (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Temperature</th>
              <th>Condition</th>
              <th>Humidity</th>
              <th>Wind Speed</th>
            </tr>
          </thead>
          <tbody>
            {data.data.map((item, index) => (
              <tr key={index}>
                <td>{item.date || item.timestamp}</td>
                <td>{item.temperature || item.temp_c}°C</td>
                <td>{item.condition || item.description}</td>
                <td>{item.humidity}%</td>
                <td>{item.wind_speed || item.wind_kph} km/h</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
    return <p>No weather data available</p>;
  };

  const renderStocksData = (data) => {
    // Handle array of stock data points
    if (Array.isArray(data) && data.length > 0) {
      return (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Open</th>
              <th>High</th>
              <th>Low</th>
              <th>Close</th>
              <th>Volume</th>
              <th>Symbol</th>
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 50).map((item, index) => (
              <tr key={index}>
                <td>{item.date || 'N/A'}</td>
                <td>${item.open || 'N/A'}</td>
                <td>${item.high || 'N/A'}</td>
                <td>${item.low || 'N/A'}</td>
                <td>${item.close || 'N/A'}</td>
                <td>{item.volume?.toLocaleString() || 'N/A'}</td>
                <td>{item.symbol || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (data.quote) {
      // Stock quote data
      return (
        <table>
          <thead>
            <tr>
              <th>Property</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Symbol</td><td>{data.quote?.symbol}</td></tr>
            <tr><td>Price</td><td>${data.quote?.price}</td></tr>
            <tr><td>Change</td><td>{data.quote?.change}</td></tr>
            <tr><td>Change Percent</td><td>{data.quote?.change_percent}</td></tr>
            <tr><td>Volume</td><td>{data.quote?.volume?.toLocaleString()}</td></tr>
            <tr><td>Market Cap</td><td>${data.quote?.market_cap?.toLocaleString()}</td></tr>
            <tr><td>Last Updated</td><td>{data.quote?.latest_trading_day}</td></tr>
          </tbody>
        </table>
      );
    } else if (data.data && Array.isArray(data.data)) {
      // Formatted stock data from backend
      return (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Open</th>
              <th>High</th>
              <th>Low</th>
              <th>Close</th>
              <th>Volume</th>
            </tr>
          </thead>
          <tbody>
            {data.data.slice(0, 50).map((item, index) => (
              <tr key={index}>
                <td>{item.date}</td>
                <td>${item.open}</td>
                <td>${item.high}</td>
                <td>${item.low}</td>
                <td>${item.close}</td>
                <td>{item.volume?.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (data.data) {
      // Daily stock data
      const timeSeries = data.data['Time Series (Daily)'] || data.data;
      const dates = Object.keys(timeSeries).slice(0, 10); // Show first 10 days
      
      return (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Open</th>
              <th>High</th>
              <th>Low</th>
              <th>Close</th>
              <th>Volume</th>
            </tr>
          </thead>
          <tbody>
            {dates.map(date => (
              <tr key={date}>
                <td>{date}</td>
                <td>${timeSeries[date]['1. open']}</td>
                <td>${timeSeries[date]['2. high']}</td>
                <td>${timeSeries[date]['3. low']}</td>
                <td>${timeSeries[date]['4. close']}</td>
                <td>{parseInt(timeSeries[date]['5. volume']).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (data.overview) {
      // Company overview
      return (
        <table>
          <thead>
            <tr>
              <th>Property</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Name</td><td>{data.overview?.Name}</td></tr>
            <tr><td>Symbol</td><td>{data.overview?.Symbol}</td></tr>
            <tr><td>Description</td><td>{data.overview?.Description}</td></tr>
            <tr><td>Industry</td><td>{data.overview?.Industry}</td></tr>
            <tr><td>Sector</td><td>{data.overview?.Sector}</td></tr>
            <tr><td>Market Cap</td><td>${data.overview?.MarketCapitalization}</td></tr>
            <tr><td>P/E Ratio</td><td>{data.overview?.PERatio}</td></tr>
            <tr><td>Dividend Yield</td><td>{data.overview?.DividendYield}</td></tr>
          </tbody>
        </table>
      );
    }
    return <p>No stock data available</p>;
  };

  const renderNewsData = (data) => {
    if (data.articles && Array.isArray(data.articles)) {
      return (
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Source</th>
              <th>Published</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {data.articles.slice(0, 10).map((article, index) => (
              <tr key={index}>
                <td>
                  <a href={article.url} target="_blank" rel="noopener noreferrer">
                    {article.title}
                  </a>
                </td>
                <td>{article.source?.name || article.source}</td>
                <td>{new Date(article.published_at || article.publishedAt).toLocaleDateString()}</td>
                <td>{article.description?.substring(0, 100)}...</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (data.trending) {
      return (
        <table>
          <thead>
            <tr>
              <th>Topic</th>
              <th>Category</th>
              <th>Country</th>
            </tr>
          </thead>
          <tbody>
            {data.trending.map((topic, index) => (
              <tr key={index}>
                <td>{topic.topic}</td>
                <td>{topic.category}</td>
                <td>{topic.country}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
    return null;
  };

  const renderImagesData = (data) => {
    if (data.photos) {
      return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}>
          {data.photos.slice(0, 12).map((photo, index) => (
            <div key={index} style={{ border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
              <img 
                src={photo.src?.medium || photo.src?.small} 
                alt={photo.alt || 'Image'} 
                style={{ width: '100%', height: '150px', objectFit: 'cover' }}
              />
              <div style={{ padding: '0.5rem' }}>
                <p style={{ fontSize: '0.9rem', margin: 0, color: '#666' }}>
                  {photo.photographer}
                </p>
              </div>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  const renderGenericData = (data) => {
    if (Array.isArray(data)) {
      if (data.length === 0) return <p>No data available</p>;
      
      const firstItem = data[0];
      const keys = Object.keys(firstItem);
      
      return (
        <table>
          <thead>
            <tr>
              {keys.map(key => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 20).map((item, index) => (
              <tr key={index}>
                {keys.map(key => (
                  <td key={key}>{JSON.stringify(item[key])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else if (typeof data === 'object') {
      return (
        <table>
          <thead>
            <tr>
              <th>Property</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(data).map(([key, value]) => (
              <tr key={key}>
                <td>{key}</td>
                <td>{typeof value === 'object' ? JSON.stringify(value) : String(value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
    
    return <p>No data to display</p>;
  };

  if (!data) return null;

  return (
    <div className="dataset-table">
      <div className="table-header">
        {dataType ? `${dataType.charAt(0).toUpperCase() + dataType.slice(1)} Data` : 'Dataset'}
      </div>
      <div className="table-content">
        {renderTableContent()}
      </div>
    </div>
  );
};

export default DatasetTable;
