# Smart Dataset Generator Frontend

A React frontend for the Smart Dataset Generator project with full backend integration and dataset download functionality.

## Features

- **Weather Data**: Get current weather, forecasts, and weather by coordinates
- **Stock Market Data**: Real-time quotes, daily data, and company overviews
- **News Data**: Top headlines, search news, and trending topics
- **Image Data**: Search images, curated collections, and category-based images
- **AI Chatbot**: OpenRouter-powered assistant for dataset generation suggestions
- **Data Export**: Download datasets in CSV, JSON, and Parquet formats
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Build for Production**:
   ```bash
   npm run build
   ```

## Backend Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000`. Make sure the backend is running before starting the frontend.

### API Endpoints Used:
- `/api/weather/*` - Weather data endpoints
- `/api/stocks/*` - Stock market data endpoints  
- `/api/news/*` - News data endpoints
- `/api/images/*` - Image data endpoints
- `/api/covid/*` - COVID-19 data endpoints
- `/chatbot/*` - AI chatbot endpoints
- `/download/*` - Data download endpoints

## Components

### Core Components
- `Navbar.jsx` - Navigation bar with links
- `Footer.jsx` - Footer with additional links
- `HeroSection.jsx` - Welcome section with tagline

### Form Components
- `WeatherForm.jsx` - Weather data collection forms
- `StocksForm.jsx` - Stock market data forms
- `NewsForm.jsx` - News data search forms
- `ImagesForm.jsx` - Image search and curation forms

### Data Components
- `DatasetTable.jsx` - Displays API results in structured tables
- `DownloadSection.jsx` - Handles data export functionality
- `ChatWidget.jsx` - AI-powered chatbot for suggestions

### API Integration
- `api/api.js` - Complete API integration layer with all backend endpoints

## Styling

The application uses CSS classes for styling with a clean, modern design:
- Responsive grid layouts
- Card-based form design
- Interactive tables with hover effects
- Fixed chat widget
- Download buttons with different colors for each format

## Future Improvements

The following components can be enhanced for better UI/UX:

### HeroSection.jsx
- Add background images or gradients
- Improve typography and spacing
- Add call-to-action buttons

### Navbar.jsx
- Add brand logo
- Improve color scheme
- Add active state indicators

### Footer.jsx
- Add social media links
- Improve link organization
- Add company information

### Forms
- Add input validation styling
- Improve button hover effects
- Add loading states with spinners
- Add form field icons

### DatasetTable.jsx
- Add table sorting functionality
- Improve row hover effects
- Add pagination for large datasets
- Add column resizing

### DownloadSection.jsx
- Add download progress indicators
- Improve button styling
- Add format descriptions

### ChatWidget.jsx
- Add typing indicators
- Improve message bubble styling
- Add emoji support
- Add message timestamps

### Global Styling (index.css)
- Add CSS variables for consistent theming
- Improve responsive breakpoints
- Add dark mode support
- Add animation transitions

## Development

The project uses Vite for fast development and building. The development server includes proxy configuration to connect to the backend API.

### Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - see LICENSE file for details.
