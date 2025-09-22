import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HeroSection from './components/HeroSection';
import WeatherForm from './components/WeatherForm';
import StocksForm from './components/StocksForm';
import NewsForm from './components/NewsForm';
import ImagesForm from './components/ImagesForm';
import ChatWidget from './components/ChatWidget';
import DatasetTable from './components/DatasetTable';
import DownloadSection from './components/DownloadSection';
import BackendStatus from './components/BackendStatus';
import DownloadTest from './components/DownloadTest';
import ErrorBoundary from './components/ErrorBoundary';

function App() {
  const [currentData, setCurrentData] = useState(null);
  const [dataType, setDataType] = useState(null);
  const [originalParams, setOriginalParams] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDataUpdate = (data, type, params = {}) => {
    setCurrentData(data);
    setDataType(type);
    setOriginalParams(params);
    setError(null);
  };

  const handleError = (errorMessage) => {
    console.error('App error:', errorMessage);
    setError(errorMessage);
    setCurrentData(null);
    setOriginalParams({});
  };

  const handleLoading = (loading) => {
    setIsLoading(loading);
  };

  return (
    <ErrorBoundary>
      <div className="app">
        <BackendStatus />
        <Navbar />
        <main className="main-content">
          <HeroSection />
          
          <div className="forms-section">
            <div className="form-grid">
              <ErrorBoundary>
                <WeatherForm 
                  onDataUpdate={handleDataUpdate}
                  onError={handleError}
                  onLoading={handleLoading}
                />
              </ErrorBoundary>
              <ErrorBoundary>
                <StocksForm 
                  onDataUpdate={handleDataUpdate}
                  onError={handleError}
                  onLoading={handleLoading}
                />
              </ErrorBoundary>
              <ErrorBoundary>
                <NewsForm 
                  onDataUpdate={handleDataUpdate}
                  onError={handleError}
                  onLoading={handleLoading}
                />
              </ErrorBoundary>
              <ErrorBoundary>
                <ImagesForm 
                  onDataUpdate={handleDataUpdate}
                  onError={handleError}
                  onLoading={handleLoading}
                />
              </ErrorBoundary>
            </div>
          </div>

        {error && (
          <div className="error-message">
            <p><strong>Error:</strong> {error}</p>
            <button 
              onClick={() => setError(null)} 
              style={{ 
                marginTop: '0.5rem', 
                padding: '0.5rem 1rem', 
                background: 'rgba(255,255,255,0.2)', 
                border: 'none', 
                borderRadius: '3px', 
                color: 'white', 
                cursor: 'pointer' 
              }}
            >
              Dismiss
            </button>
          </div>
        )}

        {isLoading && (
          <div className="loading-message">
            <p>Loading data...</p>
          </div>
        )}

        {currentData && (
          <div className="results-section">
            <ErrorBoundary>
              <DatasetTable data={currentData} dataType={dataType} />
            </ErrorBoundary>
            <ErrorBoundary>
              <DownloadSection 
                data={currentData} 
                dataType={dataType}
                originalParams={originalParams}
                onError={handleError}
              />
            </ErrorBoundary>
          </div>
        )}

        <ErrorBoundary>
          <ChatWidget />
        </ErrorBoundary>
        <DownloadTest />
      </main>
      <Footer />
    </div>
    </ErrorBoundary>
  );
}

export default App;
