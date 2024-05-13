import re


def extract_domain_link(url):
    """Extracts domain or subdomain links from full links."""
    # Using regular expression to extract domain/subdomain from full link
    match = re.search(r'(?<=://)([\w\.-]+)', url)
    if match:
        domain = match.group()
        # Remove 'www' subdomain from domain
        if domain.startswith('www.'):
            domain = domain.replace('www.', '')
        return domain
    return url