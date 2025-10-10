"""
Custom template tags for evaluations app.
"""
from django import template

register = template.Library()


@register.filter
def range_from_one(value):
    """
    Create a range from 1 to value (inclusive).

    Usage:
        {% for i in question.max_score|range_from_one %}
            {{ i }}
        {% endfor %}
    """
    try:
        return range(1, int(value) + 1)
    except (ValueError, TypeError):
        return range(1, 6)  # Default to 1-5


@register.filter
def get_item(dictionary, key):
    """
    Get item from dictionary.

    Usage:
        {{ my_dict|get_item:my_key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.simple_tag
def score_label(score_value, max_score):
    """
    Get label for score value.

    Usage:
        {% score_label 1 5 %}  -> "Çox Zəif"
        {% score_label 5 5 %}  -> "Əla"
    """
    try:
        score = int(score_value)
        max_val = int(max_score)

        # Calculate percentage
        percentage = (score / max_val) * 100

        if percentage <= 20:
            return "Çox Zəif"
        elif percentage <= 40:
            return "Zəif"
        elif percentage <= 60:
            return "Orta"
        elif percentage <= 80:
            return "Yaxşı"
        else:
            return "Əla"
    except (ValueError, TypeError):
        return ""


@register.inclusion_tag('evaluations/includes/rating_scale.html')
def render_rating_scale(question, existing_response=None):
    """
    Render a rating scale for a question.

    Usage:
        {% render_rating_scale question existing_response %}
    """
    max_score = question.max_score if question.max_score else 5
    current_score = None

    if existing_response and existing_response.score:
        current_score = existing_response.score

    return {
        'question': question,
        'max_score': max_score,
        'current_score': current_score,
        'score_range': range(1, max_score + 1),
    }


@register.filter
def percentage(value, total):
    """
    Calculate percentage.

    Usage:
        {{ completed|percentage:total }}
    """
    try:
        if int(total) == 0:
            return 0
        return round((int(value) / int(total)) * 100, 2)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
