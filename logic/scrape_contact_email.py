from flask import request, jsonify
from logic.scraping.get_contact_page import get_contact_page
from logic.scraping.request_web import request_web
from logic.utils.validate_email import  validate_email
from logic.utils.extract_domain_link import extract_domain_link
from logic.app_logger import logger


def scrape_contact_email():
    website_url = request.json.get('website_url')
    if not website_url:
        return jsonify({'error': 'Website URL is required'}), 400
    
    domain = extract_domain_link(website_url)
    contact_url = get_contact_page(domain)
    if contact_url:
        email = request_web(contact_url)
        if email:
            is_valid = validate_email(email)
            logger.info(f'Email: {email} is valid: {is_valid}')
            return jsonify({'email': email, 'is_valid': is_valid}), 200
        else:
            logger.error('Email not found')
            return jsonify({'error': 'Email not found'}), 404
    else:
        logger.error('Contact page not found')
        return jsonify({'error': 'Contact page not found'}), 404
