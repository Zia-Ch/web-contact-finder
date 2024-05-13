import re

import dns.resolver

from logic.app_logger import logger


def validate_email(email):
    # Check email syntax using regular expression
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False

    # Extract domain from email address
    _, domain = email.split('@')

    # Check domain MX records
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if mx_records:
            return True
        else:
            return False
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers) as e:
        logger.error(f"Error validating email {email}: {e}")
        return False
