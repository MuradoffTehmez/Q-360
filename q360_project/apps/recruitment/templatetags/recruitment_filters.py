"""Custom template filters for recruitment app."""
from django import template

register = template.Library()


@register.filter(name='split')
def split(value, arg):
    """Split a string by the given separator."""
    if value:
        return [item.strip() for item in value.split(arg) if item.strip()]
    return []


@register.filter(name='mul')
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
