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
