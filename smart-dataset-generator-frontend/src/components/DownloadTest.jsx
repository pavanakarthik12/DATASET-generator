import React from 'react';
import { downloadFile } from '../api/api';

const DownloadTest = () => {
  const testDownload = (format) => {
    const testData = {
      test: 'data',
      timestamp: new Date().toISOString(),
      items: [
        { id: 1, name: 'Item 1', value: 100 },
        { id: 2, name: 'Item 2', value: 200 }
      ]
    };

    try {
      if (format === 'json') {
        const jsonData = JSON.stringify(testData, null, 2);
        const blob = new Blob([jsonData], { type: 'application/json' });
        downloadFile(blob, 'test_data.json');
      } else if (format === 'csv') {
        const csvData = 'id,name,value\n1,Item 1,100\n2,Item 2,200';
        const blob = new Blob([csvData], { type: 'text/csv' });
        downloadFile(blob, 'test_data.csv');
      }
    } catch (error) {
      console.error('Test download failed:', error);
    }
  };

  return (
    <div style={{ 
      position: 'fixed', 
      bottom: '80px', 
      right: '20px', 
      background: 'white', 
      padding: '1rem', 
      border: '1px solid #ddd', 
      borderRadius: '5px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      zIndex: 999
    }}>
      <h4 style={{ margin: '0 0 0.5rem 0', fontSize: '0.9rem' }}>Download Test</h4>
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <button 
          onClick={() => testDownload('json')}
          style={{ 
            padding: '0.25rem 0.5rem', 
            fontSize: '0.8rem',
            background: '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '3px',
            cursor: 'pointer'
          }}
        >
          Test JSON
        </button>
        <button 
          onClick={() => testDownload('csv')}
          style={{ 
            padding: '0.25rem 0.5rem', 
            fontSize: '0.8rem',
            background: '#27ae60',
            color: 'white',
            border: 'none',
            borderRadius: '3px',
            cursor: 'pointer'
          }}
        >
          Test CSV
        </button>
      </div>
    </div>
  );
};

export default DownloadTest;
