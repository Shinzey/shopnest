"""
Django templates custom filters and tags.
"""
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)
    return 0

@register.filter
def mul(value, arg):
    """Multiply value by argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
