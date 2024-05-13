import re

from bs4 import BeautifulSoup


def get_email(page_source):
    """Finds the email from a given page source using multiple methods."""
    # Method 1: Search for email in simple text format
    email_text = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_source)
    if email_text:
        return email_text.group()

    # Method 2: Search for email in hyperlinks
    email_link = re.search(r'href="mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})"', page_source)
    if email_link:
        return email_link.group(1)
    
    # Method 3: Search for email in href links
    soup = BeautifulSoup(page_source, 'html.parser')
    email_anchors = soup.find_all('a', href=re.compile(r'^mailto:'))
    for anchor in email_anchors:
        email = anchor.get('href').replace('mailto:', '').strip()
        if re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
            return email

    # Method 4: Search for email in parent elements of anchor tags
    for anchor in email_anchors:
        parent_element = anchor.find_parent()
        if parent_element and parent_element.text:
            email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', parent_element.text)
            if email:
                return email.group()
            
    # Look for text containing "Email" near the footer
    footer_text = re.search(r'<footer[^>]*>(.*?)</footer>', page_source, re.DOTALL)
    if footer_text:
        if '@' in footer_text.group(1).lower():  
            email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', footer_text.group(1))      
           
    return None