# unitsvalue/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def to_persian_number(value):
    if isinstance(value, (int, float, str)):
        # Convert string to int/float if necessary
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        result = ''.join(persian_digits[int(digit)] if digit.isdigit() else digit for digit in str(value))
        return result
    return value