from django import template

register = template.Library()

@register.filter
def split(value, separator=' '):
    """
    Splits a string into a list using the given separator.
    Example: {{ value|split:"," }}
    """
    if not value:
        return []
    return value.split(separator)

@register.filter
def multiply(value, arg):
    """
    Multiplies two values in templates
    Example: {{ price|multiply:quantity }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
