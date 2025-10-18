"""Custom template filters for navigation helpers."""
from django import template

register = template.Library()


@register.filter(name="startswith")
def startswith(value, prefix):
    """Return True if the given value starts with the provided prefix."""
    if value is None or prefix is None:
        return False
    return str(value).startswith(str(prefix))
