# Web Scraping Full Stack Project Documentation

## Project Overview
This project uses Crawl4AI, a powerful LLM-friendly web crawler, integrated with a React frontend for efficient web scraping operations.

## Project Structure
```
full-stack-react-scrapping/
├── frontend/          # React + Vite application
│   ├── src/          # React source files
│   ├── public/       # Static assets
│   ├── package.json  # Frontend dependencies
│   └── vite.config.js # Vite configuration
├── backend/          # Flask application
│   ├── venv/        # Python virtual environment
│   ├── app.py       # Flask application
│   └── requirements.txt # Python dependencies
└── AppInfo.md       # This documentation file
```

## Technology Stack
- Frontend:
  - React (Vite)
  - Tailwind CSS
  - Shadcn UI

- Backend:
  - Flask
  - Crawl4AI (v0.4.24)
  - Pandas (for data processing)

## Current Status

### Frontend
- Running on: http://localhost:5173
- Status: Fully configured with Tailwind CSS
- Proxy: Configured for API calls
- UI Framework: Shadcn UI installed

### Backend
- Running on: http://127.0.0.1:5000
- Status: Running with debug mode enabled
- Virtual Environment: Properly configured in `backend/venv`
- Dependencies: Updated to use Crawl4AI
- API Endpoints:
  - `/api/health`: Health check endpoint
    - Returns: JSON with status and installed dependencies
  - `/api/scrape`: Web scraping endpoint (POST)
    - Input: JSON with `url` field
    - Returns: Markdown and filtered content

### Crawl4AI Integration
- Version: 0.4.24
- Features Implemented:
  - Headless browser automation
  - Markdown generation with content filtering
  - Caching enabled for better performance
  - Error handling and status reporting

### Environment Verification
```json
// GET http://127.0.0.1:5000/api/health response:
{
    "dependencies": {
        "crawl4ai": "installed",
        "requests": "installed",
        "pandas": "installed"
    },
    "message": "Scraping backend is running!",
    "status": "healthy"
}
```

## API Documentation

### POST /api/scrape
Endpoint for web scraping operations.

Request body:
```json
{
    "url": "https://example.com"
}
```

Response:
```json
{
    "status": "success",
    "markdown": "...",
    "fit_markdown": "...",
    "length": {
        "markdown": 1234,
        "fit_markdown": 567
    }
}
```

## Next Steps
1. Frontend Development:
   - Create scraping form component
   - Add markdown preview
   - Implement loading states
   - Add error handling UI

2. Backend Enhancements:
   - Add rate limiting
   - Implement concurrent scraping
   - Add custom extraction strategies
   - Set up data export functionality

3. Features to Implement:
   - Scheduled scraping
   - Custom filtering options
   - Data visualization
   - Export to various formats

## Running the Application
1. Start Backend:
```bash
cd backend
venv\Scripts\activate
python app.py
```

2. Start Frontend:
```bash
cd frontend
npm run dev
