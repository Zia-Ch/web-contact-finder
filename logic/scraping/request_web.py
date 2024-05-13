import requests
from fake_useragent import UserAgent

from logic.scraping.get_email import get_email

def request_web(url):
   
    """Finds the contact email from the contact page of a given URL."""
    # Define headers with a rotating user agent
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        page_source = response.text
        
        # Find the email using the provided function
        email = get_email(page_source)
        return email
    except Exception as e:
        print(e)
        return None  