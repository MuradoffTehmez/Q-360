"""
Wellness App Custom Template Tags and Filters
"""
from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiply the value by the argument.
    Usage: {{ value|multiply:20 }}

    Args:
        value: The number to multiply
        arg: The multiplier

    Returns:
        The product of value and arg
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='percentage')
def percentage(value, total=100):
    """
    Calculate percentage.
    Usage: {{ value|percentage:total }}

    Args:
        value: The current value
        total: The total value (default: 100)

    Returns:
        Percentage as float
    """
    try:
        if float(total) == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter(name='divide')
def divide(value, arg):
    """
    Divide the value by the argument.
    Usage: {{ value|divide:2 }}

    Args:
        value: The dividend
        arg: The divisor

    Returns:
        The quotient
    """
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter(name='subtract')
def subtract(value, arg):
    """
    Subtract the argument from value.
    Usage: {{ value|subtract:5 }}

    Args:
        value: The number to subtract from
        arg: The number to subtract

    Returns:
        The difference
    """
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
