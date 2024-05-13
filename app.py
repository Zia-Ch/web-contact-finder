import os
from flask import Flask, jsonify
from flask_limiter import Limiter
from werkzeug.exceptions import HTTPException

from logic.app_logger import logger
from logic.scrape_contact_email import scrape_contact_email



app = Flask(__name__)

# Enable debug mode during development
app.debug = True

# Set a secret key for session management
app.secret_key = os.urandom(24)

# Implement rate limiting
limiter = Limiter(
    app,
    #key_func=get_remote_address,
    default_limits=["1000/day"]
)


 
@limiter.limit("10/minute")
@app.route('/api', methods=['POST'])

def api():
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
