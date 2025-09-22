import React, { useState, useEffect } from 'react';

const BackendStatus = () => {
  const [status, setStatus] = useState('checking');
  const [lastChecked, setLastChecked] = useState(null);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setStatus('connected');
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('disconnected');
    }
    setLastChecked(new Date());
  };

  useEffect(() => {
    checkBackendStatus();
    // Check every 30 seconds
    const interval = setInterval(checkBackendStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'connected': return '#27ae60';
      case 'disconnected': return '#e74c3c';
      case 'error': return '#f39c12';
      default: return '#95a5a6';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected': return 'Backend Connected';
      case 'disconnected': return 'Backend Disconnected';
      case 'error': return 'Backend Error';
      default: return 'Checking...';
    }
  };

  return (
    <div 
      style={{
        position: 'fixed',
        top: '10px',
        right: '10px',
        background: 'white',
        padding: '0.5rem 1rem',
        borderRadius: '5px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        border: `2px solid ${getStatusColor()}`,
        fontSize: '0.9rem',
        zIndex: 1000,
        cursor: 'pointer'
      }}
      onClick={checkBackendStatus}
      title="Click to check backend status"
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <div 
          style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: getStatusColor()
          }}
        />
        <span style={{ color: getStatusColor(), fontWeight: 'bold' }}>
          {getStatusText()}
        </span>
      </div>
      {lastChecked && (
        <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.25rem' }}>
          Last checked: {lastChecked.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};

export default BackendStatus;
