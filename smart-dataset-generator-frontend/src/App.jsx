import React, { useEffect, useState } from 'react'
import HeroSection from './components/HeroSection'
import WeatherForm from './components/WeatherForm'
import StocksForm from './components/StocksForm'
import NewsForm from './components/NewsForm'
import ImagesForm from './components/ImagesForm'
import ChatWidget from './components/ChatWidget'
import DatasetTable from './components/DatasetTable'
import DownloadSection from './components/DownloadSection'
import BackendStatus from './components/BackendStatus';
import ErrorBoundary from './components/ErrorBoundary';
// Removed Tabs components import because ./components/ui/tabs does not exist

const cn = (...classes) => classes.filter(Boolean).join(" ");

function App() {
    const [currentData, setCurrentData] = useState(null);
    const [dataType, setDataType] = useState(null);
    const [originalParams, setOriginalParams] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeSource, setActiveSource] = useState('all');

    // Ensure when navigating from the hero CTA, we land on the forms section
    useEffect(() => {
        // If the app just mounted (e.g., from "#/app"), scroll to the data section
        const scrollToData = () => {
            const dataSection = document.getElementById('data');
            if (dataSection) {
                dataSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        };

        // Try immediately and also on next frame to handle mount timing
        scrollToData();
        const id = requestAnimationFrame(scrollToData);
        return () => cancelAnimationFrame(id);
    }, []);

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

    const clearAll = () => {
        setCurrentData(null);
        setDataType(null);
        setOriginalParams({});
        setError(null);
    };

    const navigation = [
        { name: 'Data Sources', href: '#data', icon: 'database' },
        { name: 'AI Assistant', href: '#ai', icon: 'robot' },
        { name: 'Downloads', href: '#downloads', icon: 'download' },
        { name: 'Settings', href: '#settings', icon: 'settings' }
    ];

    return (
        <ErrorBoundary>
            <div className="app-container">
                <BackendStatus />
                <div className="app">
                    <aside className="sidebar">
                        <nav>
                            <ul>
                                {navigation.map(item => (
                                    <li key={item.name}>
                                        <a href={item.href} className="sidebar-link">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-database"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 1 21 19V5"/><ellipse cx="12" cy="19" rx="9" ry="3"/></svg>{item.name}
                                        </a>
                                    </li>
                                ))}
                            </ul>
                        </nav>
                    </aside>
                    <main className="main-content">
                        {/* Hero is now a separate landing page */}

                        <div id="data" data-tab="data">
                            <div className="forms-section">
                                <header className="forms-header">
                                    <h2>Create your dataset</h2>
                                    <p>Pick a source below, set a few options, and generate. You can mix and match sources and export when ready.</p>
                                </header>
                                <div className="forms-toolbar">
                                    <div className="toolbar-left">
                                        <span className="toolbar-label">Sources</span>
                                        <nav className="toolbar-chips" aria-label="Quick jump to source">
                                            <button type="button" className={`chip ${activeSource==='all' ? 'active' : ''}`} onClick={() => setActiveSource('all')}>All</button>
                                            <button type="button" className={`chip ${activeSource==='weather' ? 'active' : ''}`} onClick={() => setActiveSource('weather')}>Weather</button>
                                            <button type="button" className={`chip ${activeSource==='stocks' ? 'active' : ''}`} onClick={() => setActiveSource('stocks')}>Stocks</button>
                                            <button type="button" className={`chip ${activeSource==='news' ? 'active' : ''}`} onClick={() => setActiveSource('news')}>News</button>
                                            <button type="button" className={`chip ${activeSource==='images' ? 'active' : ''}`} onClick={() => setActiveSource('images')}>Images</button>
                                        </nav>
                                    </div>
                                    <div className="toolbar-right">
                                        {currentData ? (
                                            <span className="toolbar-status">Ready • {Array.isArray(currentData) ? currentData.length : 1} rows</span>
                                        ) : (
                                            <span className="toolbar-status muted">No dataset yet</span>
                                        )}
                                        <button className="btn btn-ghost" onClick={clearAll}>Clear All</button>
                                        <button className="btn btn-primary" onClick={() => {
                                            const el = document.getElementById('downloads');
                                            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                                        }} disabled={!currentData}>Go to Downloads</button>
                                    </div>
                                </div>
                                <div className="form-grid">
                                    {(activeSource==='all' || activeSource==='weather') && (
                                        <ErrorBoundary>
                                            <WeatherForm
                                                onDataUpdate={handleDataUpdate}
                                                onError={handleError}
                                                onLoading={handleLoading}
                                            />
                                        </ErrorBoundary>
                                    )}
                                    {(activeSource==='all' || activeSource==='stocks') && (
                                        <ErrorBoundary>
                                            <StocksForm
                                                onDataUpdate={handleDataUpdate}
                                                onError={handleError}
                                                onLoading={handleLoading}
                                            />
                                        </ErrorBoundary>
                                    )}
                                    {(activeSource==='all' || activeSource==='news') && (
                                        <ErrorBoundary>
                                            <NewsForm
                                                onDataUpdate={handleDataUpdate}
                                                onError={handleError}
                                                onLoading={handleLoading}
                                            />
                                        </ErrorBoundary>
                                    )}
                                    {(activeSource==='all' || activeSource==='images') && (
                                        <ErrorBoundary>
                                            <ImagesForm
                                                onDataUpdate={handleDataUpdate}
                                                onError={handleError}
                                                onLoading={handleLoading}
                                            />
                                        </ErrorBoundary>
                                    )}
                                </div>
                            </div>
                        </div>

                        <div data-tab="ai">
                            <ErrorBoundary>
                                <ChatWidget />
                            </ErrorBoundary>
                        </div>

                        <div id="downloads" data-tab="downloads">
                            {error && (
                                <div className="error-message">
                                    <p>
                                        <strong>Error:</strong> {error}
                                    </p>
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
                        </div>

                        <div data-tab="settings">
                            <div>Settings Content</div>
                        </div>
                    </main>
                </div>
            </div>
        </ErrorBoundary>
    );
}

export default App;
