import React, { useState } from 'react';
import { imagesAPI } from '../api/api';

const ImagesForm = ({ onDataUpdate, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    query: '',
    perPage: 15,
    orientation: '',
    color: '',
    category: ''
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
      const perPage = parseInt(formData.perPage);
      
      if (isNaN(perPage) || perPage < 1 || perPage > 80) {
        throw new Error('Number of images must be between 1 and 80');
      }
      
      if (searchType === 'search') {
        if (!formData.query.trim()) {
          throw new Error('Search query is required');
        }
        if (formData.query.trim().length < 2) {
          throw new Error('Search query must be at least 2 characters');
        }
        response = await imagesAPI.searchImages(
          formData.query.trim(), 
          perPage,
          formData.orientation || null,
          formData.color || null
        );
      } else if (searchType === 'curated') {
        response = await imagesAPI.getCuratedImages(perPage);
      } else if (searchType === 'category') {
        if (!formData.category.trim()) {
          throw new Error('Category is required');
        }
        response = await imagesAPI.getImagesByCategory(
          formData.category, 
          perPage
        );
      }

      if (response.success && response.data) {
        const params = {
          query: formData.query.trim(),
          perPage: perPage,
          orientation: formData.orientation,
          color: formData.color,
          category: formData.category
        };
        onDataUpdate(response.data, 'images', params);
      } else {
        throw new Error(response.error || response.detail || 'Failed to fetch images');
      }
    } catch (error) {
      onError(error.message);
    } finally {
      onLoading(false);
    }
  };

  return (
    <div className="form-card" id="images">
      <h3>Image Data</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Search Type:</label>
          <select 
            value={searchType} 
            onChange={(e) => setSearchType(e.target.value)}
          >
            <option value="search">Search Images</option>
            <option value="curated">Curated Images</option>
            <option value="category">Images by Category</option>
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
              placeholder="e.g., nature, technology, food"
              required
            />
          </div>
        )}

        {searchType === 'category' && (
          <div className="form-group">
            <label htmlFor="category">Category:</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              required
            >
              <option value="">Select Category</option>
              <option value="nature">Nature</option>
              <option value="technology">Technology</option>
              <option value="business">Business</option>
              <option value="people">People</option>
              <option value="animals">Animals</option>
              <option value="food">Food</option>
              <option value="travel">Travel</option>
              <option value="architecture">Architecture</option>
              <option value="abstract">Abstract</option>
            </select>
          </div>
        )}

        <div className="form-group">
          <label htmlFor="perPage">Number of Images:</label>
          <input
            type="number"
            id="perPage"
            name="perPage"
            value={formData.perPage}
            onChange={handleInputChange}
            min="1"
            max="80"
            required
          />
        </div>

        {searchType === 'search' && (
          <>
            <div className="form-group">
              <label htmlFor="orientation">Orientation (Optional):</label>
              <select
                id="orientation"
                name="orientation"
                value={formData.orientation}
                onChange={handleInputChange}
              >
                <option value="">Any Orientation</option>
                <option value="landscape">Landscape</option>
                <option value="portrait">Portrait</option>
                <option value="square">Square</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="color">Color (Optional):</label>
              <select
                id="color"
                name="color"
                value={formData.color}
                onChange={handleInputChange}
              >
                <option value="">Any Color</option>
                <option value="red">Red</option>
                <option value="orange">Orange</option>
                <option value="yellow">Yellow</option>
                <option value="green">Green</option>
                <option value="turquoise">Turquoise</option>
                <option value="blue">Blue</option>
                <option value="violet">Violet</option>
                <option value="pink">Pink</option>
                <option value="brown">Brown</option>
                <option value="black">Black</option>
                <option value="gray">Gray</option>
                <option value="white">White</option>
              </select>
            </div>
          </>
        )}

        <button type="submit" className="form-button">
          Get Images
        </button>
      </form>
    </div>
  );
};

export default ImagesForm;
