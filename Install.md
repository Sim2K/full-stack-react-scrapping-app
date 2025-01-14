# Web Scraping Full Stack Project Installation Guide

This guide provides step-by-step instructions for setting up the web scraping project with React frontend and Flask backend, using Crawl4AI.

## Prerequisites
- Node.js (Latest LTS version)
- Python 3.8 or higher
- Git (optional but recommended)

## Step 1: Project Setup
```bash
# Create project directory
mkdir full-stack-react-scrapping
cd full-stack-react-scrapping
```

## Step 2: Frontend Setup
```bash
# Create React + Vite project
npm create vite@latest frontend --template react

# Navigate to frontend directory
cd frontend

# Install base dependencies
npm install

# Install Tailwind CSS and its dependencies
npm install -D tailwindcss postcss autoprefixer
npm install -D tailwindcss-animate class-variance-authority clsx tailwind-merge

# Initialize Tailwind CSS
npx tailwindcss init -p

# Install Shadcn UI
npm install -D @shadcn/ui
```

### Frontend Configuration Files

1. Update `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

2. Update `vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
```

## Step 3: Backend Setup
```bash
# Create backend directory
mkdir backend
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

Create `requirements.txt` with the following content:
```
flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
crawl4ai==0.4.24
requests==2.31.0
pandas==2.1.4
```

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright (required for Crawl4AI)
python -m playwright install --with-deps chromium
```

Create `app.py` with the following content:
```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Scraping backend is running!',
        'dependencies': {
            'crawl4ai': 'installed',
            'requests': 'installed',
            'pandas': 'installed'
        }
    })

@app.route('/api/scrape', methods=['POST'])
async def scrape():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        browser_config = BrowserConfig(
            headless=True,
            verbose=True
        )
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.ENABLED,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(
                    threshold=0.48,
                    threshold_type="fixed",
                    min_word_threshold=0
                )
            )
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )

            return jsonify({
                'status': 'success',
                'markdown': result.markdown,
                'fit_markdown': result.fit_markdown,
                'length': {
                    'markdown': len(result.markdown),
                    'fit_markdown': len(result.fit_markdown)
                }
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## Step 4: Running the Application

1. Start the Backend:
```bash
cd backend
venv\Scripts\activate
python app.py
```

2. Start the Frontend (in a new terminal):
```bash
cd frontend
npm run dev
```

## Verification Steps

1. Backend Health Check:
   - Visit http://127.0.0.1:5000/api/health
   - Should see a JSON response with status "healthy" and installed dependencies

2. Frontend:
   - Visit http://localhost:5173
   - Should see the React + Vite welcome page

## Testing the Scraping Functionality

You can test the scraping endpoint using curl or Postman:

```bash
curl -X POST http://localhost:5000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Common Issues and Solutions

1. If `npm run dev` fails:
   - Make sure you're in the frontend directory
   - Try deleting node_modules and running `npm install` again

2. If Flask fails to start:
   - Ensure you've activated the virtual environment
   - Check if port 5000 is already in use

3. If scraping fails:
   - Verify Playwright is installed correctly
   - Check the URL is accessible
   - Ensure you have internet connectivity

## Next Steps

After successful installation:
1. Create your first scraping component
2. Add error handling and loading states
3. Implement data visualization
4. Add export functionality
