from flask import Flask, jsonify, request
from flask_cors import CORS
import asyncio
import sys
import json
import os
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import LLMExtractionStrategy

# Set default encoding to UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

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
    instruction = data.get('instruction', '')  # Get the instruction from request
    
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
            ),
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4",
                api_token=os.getenv('OPENAI_API_KEY'),
                extraction_type="instruction",
                instruction=instruction or "Extract the main content and key information from this page in to a relevant JSON format."
            ) if instruction else None
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )

            # Prepare response data
            response_data = {
                'status': 'success',
                'markdown': result.markdown.encode('utf-8').decode('utf-8'),
                'fit_markdown': result.fit_markdown.encode('utf-8').decode('utf-8'),
                'length': {
                    'markdown': len(result.markdown),
                    'fit_markdown': len(result.fit_markdown)
                }
            }

            # Add extracted content if available
            if hasattr(result, 'extracted_content'):
                response_data['extracted_content'] = result.extracted_content

            return app.response_class(
                response=json.dumps(response_data, ensure_ascii=False),
                status=200,
                mimetype='application/json'
            )

    except Exception as e:
        error_message = str(e).encode('utf-8', errors='replace').decode('utf-8')
        return jsonify({
            'status': 'error',
            'message': error_message
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
