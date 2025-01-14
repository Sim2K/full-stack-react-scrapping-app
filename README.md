# Web Scraping Application

A full-stack web scraping application built with React, Flask, and Crawl4AI.

## Features

- Modern React frontend with Vite
- Flask backend with Crawl4AI integration
- Clean and efficient web scraping
- Markdown output generation
- Content filtering and processing

## Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- Shadcn UI

### Backend
- Flask
- Crawl4AI
- Pandas

## Getting Started

For detailed installation instructions, please see [Install.md](Install.md).

For project documentation and API details, see [AppInfo.md](AppInfo.md).

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Sim2K/full-stack-react-scrapping.git
cd full-stack-react-scrapping
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Start the application:
```bash
# Terminal 1 (Backend)
cd backend
venv\Scripts\activate
python app.py

# Terminal 2 (Frontend)
cd frontend
npm run dev
```

## License

MIT

## Author

[Sim2K](https://github.com/Sim2K)
