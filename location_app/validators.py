# validators.py
from django.core.exceptions import ValidationError
import re

def validate_email(value):
    if '@' not in value:
        raise ValidationError('Invalid email address.')
    return value

def validate_phone_number(value):
    pattern = re.compile(
        r'^(\+91[-\s]?)?[0]?[789]\d{9}$'
        r'|^040-\d{8}$'
    )
    if not pattern.match(value):
        raise ValidationError("Phone number must be a valid Indian number or in the format: '040-23231380'.")
    return value

def validate_location(value):
    if not value:
        raise ValidationError("Location cannot be empty.")
    return value
