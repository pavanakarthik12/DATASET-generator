import React, { useState } from 'react';
import { newsAPI } from '../api/api';

const NewsForm = ({ onDataUpdate, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    query: '',
    country: 'us',
    category: '',
    language: 'en',
    pageSize: 20
  });
  const [searchType, setSearchType] = useState('search');

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
      
      if (searchType === 'headlines') {
        const pageSize = parseInt(formData.pageSize);
        if (isNaN(pageSize) || pageSize < 1 || pageSize > 100) {
          throw new Error('Page size must be a number between 1 and 100');
        }
        response = await newsAPI.getTopHeadlines(
          formData.country, 
          formData.category || null, 
          pageSize
        );
      } else if (searchType === 'search') {
        if (!formData.query.trim()) {
          throw new Error('Search query is required');
        }
        if (formData.query.trim().length < 2) {
          throw new Error('Search query must be at least 2 characters');
        }
        const pageSize = parseInt(formData.pageSize);
        if (isNaN(pageSize) || pageSize < 1 || pageSize > 100) {
          throw new Error('Page size must be a number between 1 and 100');
        }
        response = await newsAPI.searchNews(
          formData.query.trim(), 
          formData.language, 
          pageSize
        );
      } else if (searchType === 'trending') {
        response = await newsAPI.getTrendingTopics(formData.country, formData.category);
      }

      if (response.success && response.data) {
        const params = {
          query: formData.query.trim(),
          country: formData.country,
          category: formData.category,
          language: formData.language,
          pageSize: parseInt(formData.pageSize)
        };
        onDataUpdate(response.data, 'news', params);
      } else {
        throw new Error(response.error || response.detail || 'Failed to fetch news data');
      }
    } catch (error) {
      onError(error.message);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="form-card" id="news">
      <h3 className="form-title">
        <svg className="form-title-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 5h16"/><path d="M4 12h16"/><path d="M4 19h16"/></svg>
        News Data
      </h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Search Type:</label>
          <select 
            value={searchType} 
            onChange={(e) => setSearchType(e.target.value)}
          >
            <option value="headlines">Top Headlines</option>
            <option value="search">Search News</option>
            <option value="trending">Trending Topics</option>
          </select>
        </div>

        {searchType === 'search' && (
          <div className="form-group">
            <label htmlFor="query">Search Query:</label>
            <input
              type="text"
              id="query"
              name="query"
              value={formData.query}
              onChange={handleInputChange}
              placeholder="e.g., technology, climate change"
              required
            />
          </div>
        )}

        <div className="form-group">
          <label htmlFor="country">Country:</label>
          <select
            id="country"
            name="country"
            value={formData.country}
            onChange={handleInputChange}
          >
            <option value="us">United States</option>
            <option value="gb">United Kingdom</option>
            <option value="ca">Canada</option>
            <option value="au">Australia</option>
            <option value="de">Germany</option>
            <option value="fr">France</option>
            <option value="in">India</option>
            <option value="jp">Japan</option>
          </select>
        </div>

        {(searchType === 'headlines' || searchType === 'trending') && (
          <div className="form-group">
            <label htmlFor="category">Category (Optional):</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
            >
              <option value="">All Categories</option>
              <option value="business">Business</option>
              <option value="entertainment">Entertainment</option>
              <option value="general">General</option>
              <option value="health">Health</option>
              <option value="science">Science</option>
              <option value="sports">Sports</option>
              <option value="technology">Technology</option>
            </select>
          </div>
        )}

        {searchType === 'search' && (
          <div className="form-group">
            <label htmlFor="language">Language:</label>
            <select
              id="language"
              name="language"
              value={formData.language}
              onChange={handleInputChange}
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="it">Italian</option>
              <option value="pt">Portuguese</option>
              <option value="ru">Russian</option>
              <option value="zh">Chinese</option>
            </select>
          </div>
        )}

        <div className="form-group">
          <label htmlFor="pageSize">Number of Articles:</label>
          <input
            type="number"
            id="pageSize"
            name="pageSize"
            value={formData.pageSize}
            onChange={handleInputChange}
            min="1"
            max="100"
            required
          />
        </div>

        <button type="submit" className="btn btn-primary btn-news">
          Get News Data
        </button>
      </form>
    </div>
  );
};

export default NewsForm;
