import re
from django.core.exceptions import ValidationError


def check_website(website):
    """
        website validator
    """
    pattern = '^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$'
    if not re.search(pattern, website):
        raise ValidationError(_('your website is invalid'))
