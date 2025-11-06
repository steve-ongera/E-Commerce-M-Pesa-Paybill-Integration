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
