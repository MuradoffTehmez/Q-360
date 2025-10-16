"""Custom template filters for recruitment app."""
from django import template

register = template.Library()


@register.filter(name='split')
def split(value, arg):
    """Split a string by the given separator."""
    if value:
        return [item.strip() for item in value.split(arg) if item.strip()]
    return []
