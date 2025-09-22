import React, { useState } from 'react';
import { downloadAPI, downloadFile } from '../api/api';

const DownloadSection = ({ data, dataType, onError, originalParams = {} }) => {
  const [isDownloading, setIsDownloading] = useState({});

  const handleDownload = async (format) => {
    if (!data || !dataType) {
      onError('No data available for download');
      return;
    }

    console.log('Download request:', { dataType, format, originalParams, data });
    setIsDownloading(prev => ({ ...prev, [format]: true }));

    try {
      let blob;
      let filename;

      // For all data types, create files directly from current data
      if (format === 'json') {
        const jsonData = JSON.stringify(data, null, 2);
        blob = new Blob([jsonData], { type: 'application/json' });
        filename = `${dataType}_data_${new Date().toISOString().slice(0,10)}.json`;
      } else if (format === 'csv') {
        const csvData = convertToCSV(data);
        blob = new Blob([csvData], { type: 'text/csv' });
        filename = `${dataType}_data_${new Date().toISOString().slice(0,10)}.csv`;
      } else if (format === 'parquet') {
        // For parquet, fallback to CSV since we can't create parquet files in browser
        const csvData = convertToCSV(data);
        blob = new Blob([csvData], { type: 'text/csv' });
        filename = `${dataType}_data_${new Date().toISOString().slice(0,10)}.csv`;
      } else if (format === 'zip') {
        // For images, create a JSON file with image URLs
        const imageData = Array.isArray(data) ? data : (data.photos || []);
        const imageUrls = imageData.map(photo => ({
          url: photo.src?.original || photo.src?.large || photo.src?.medium || photo.url,
          photographer: photo.photographer,
          alt: photo.alt || photo.description
        }));
        const jsonData = JSON.stringify(imageUrls, null, 2);
        blob = new Blob([jsonData], { type: 'application/json' });
        filename = `${dataType}_urls_${new Date().toISOString().slice(0,10)}.json`;
      }

      if (blob && filename) {
        downloadFile(blob, filename);
      } else {
        throw new Error(`Download format ${format} not supported for ${dataType} data`);
      }
    } catch (error) {
      // Fallback: create file directly from current data
      try {
        console.log('Backend download failed, creating file from current data...');
        let fallbackBlob;
        let fallbackFilename;
        
        if (format === 'json') {
          const jsonData = JSON.stringify(data, null, 2);
          fallbackBlob = new Blob([jsonData], { type: 'application/json' });
          fallbackFilename = `${dataType}_data_${new Date().toISOString().slice(0,10)}.json`;
        } else if (format === 'csv') {
          const csvData = convertToCSV(data);
          fallbackBlob = new Blob([csvData], { type: 'text/csv' });
          fallbackFilename = `${dataType}_data_${new Date().toISOString().slice(0,10)}.csv`;
        } else if (format === 'parquet') {
          // For parquet, fallback to CSV since we can't create parquet files in browser
          const csvData = convertToCSV(data);
          fallbackBlob = new Blob([csvData], { type: 'text/csv' });
          fallbackFilename = `${dataType}_data_${new Date().toISOString().slice(0,10)}.csv`;
        } else if (format === 'zip') {
          // For images, create a JSON file with image URLs
          const imageData = data.photos ? data.photos.map(photo => ({
            url: photo.src?.original || photo.src?.large || photo.src?.medium,
            photographer: photo.photographer,
            alt: photo.alt
          })) : [];
          const jsonData = JSON.stringify(imageData, null, 2);
          fallbackBlob = new Blob([jsonData], { type: 'application/json' });
          fallbackFilename = `${dataType}_urls_${new Date().toISOString().slice(0,10)}.json`;
        }
        
        if (fallbackBlob && fallbackFilename) {
          downloadFile(fallbackBlob, fallbackFilename);
        } else {
          throw new Error(`Cannot create ${format} file from current data`);
        }
      } catch (fallbackError) {
        onError(`Download failed: ${error.message}. Fallback also failed: ${fallbackError.message}`);
      }
    } finally {
      setIsDownloading(prev => ({ ...prev, [format]: false }));
    }
  };

  const convertToCSV = (data) => {
    try {
      if (Array.isArray(data)) {
        if (data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csvRows = [headers.join(',')];
        
        data.forEach(row => {
          const values = headers.map(header => {
            const value = row[header];
            if (value === null || value === undefined) return '';
            if (typeof value === 'object') return `"${JSON.stringify(value)}"`;
            if (typeof value === 'string' && (value.includes(',') || value.includes('"') || value.includes('\n'))) {
              return `"${value.replace(/"/g, '""')}"`;
            }
            return value;
          });
          csvRows.push(values.join(','));
        });
        
        return csvRows.join('\n');
      } else if (typeof data === 'object') {
        const headers = Object.keys(data);
        const values = headers.map(header => {
          const value = data[header];
          if (value === null || value === undefined) return '';
          if (typeof value === 'object') return `"${JSON.stringify(value)}"`;
          if (typeof value === 'string' && (value.includes(',') || value.includes('"') || value.includes('\n'))) {
            return `"${value.replace(/"/g, '""')}"`;
          }
          return value;
        });
        return [headers.join(','), values.join(',')].join('\n');
      }
      
      return '';
    } catch (error) {
      console.error('CSV conversion error:', error);
      return 'Error converting data to CSV';
    }
  };

  const getAvailableFormats = () => {
    switch (dataType) {
      case 'weather':
        return ['csv', 'json'];
      case 'stocks':
        return ['csv', 'parquet'];
      case 'news':
        return ['csv', 'json'];
      case 'images':
        return ['zip'];
      default:
        return ['csv', 'json'];
    }
  };

  const formatLabels = {
    csv: 'CSV',
    json: 'JSON',
    parquet: 'Parquet',
    zip: 'ZIP'
  };

  const availableFormats = getAvailableFormats();

  if (!data || !dataType) return null;

  return (
    <div className="download-section">
      <h3>Download Dataset</h3>
      <div className="download-buttons">
        {availableFormats.map(format => (
          <button
            key={format}
            className={`download-btn ${format}`}
            onClick={() => handleDownload(format)}
            disabled={isDownloading[format]}
          >
            {isDownloading[format] ? 'Downloading...' : `Download ${formatLabels[format]}`}
          </button>
        ))}
      </div>
    </div>
  );
};

export default DownloadSection;
