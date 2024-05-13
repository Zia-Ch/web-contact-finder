import os
from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from werkzeug.exceptions import HTTPException

from logic.app_logger import logger
from logic.scrape_contact_email import scrape_contact_email



app = Flask(__name__)

# Enable debug mode during development
app.debug = True

# Load environment variables
load_dotenv(find_dotenv(".env"))

# Get API key from environment variable
API_KEY = os.getenv('API_KEY')


# Implement rate limiting
limiter = Limiter(
    app,
    default_limits=["20000/day"]
)


 
@limiter.limit("30/minute")
@app.route('/api', methods=['POST'])

def api():
    api_key = request.headers.get('X-API-KEY')
    
    # Validate API key
    if not api_key or not api_key == API_KEY:
        return jsonify({'error': 'Invalid API key'}), 401
    
    return scrape_contact_email()
    
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle HTTP exceptions and log errors."""
    if isinstance(e, HTTPException):
        return jsonify({'error': e.description}), e.code
    logger.exception(f"Unhandled Exception: {e}")
    return jsonify({'error': 'Internal Server Error'}), 500
            
if __name__ == "__main__":
    app.run()
