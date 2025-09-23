from django import template
import re
register = template.Library()

@register.simple_tag
def render_stars(rating, max_stars=5, filled_star='★', empty_star='☆'):
    """Render star rating as filled and empty stars."""
    filled = int(rating)
    empty = max_stars - filled
    return filled_star * filled + empty_star * empty

# Simple heuristic regex to detect any HTML-like tag
_TAG_RE = re.compile(r'<[^>]+>')

@register.filter(name='has_html')
def has_html(value):
    """Return True if value contains angle-bracket HTML-like tags.

    This is a heuristic, not a sanitizer. Use it only for styling / indication.
    Returns False for None/empty values.
    """
    if not value:
        return False
    return bool(_TAG_RE.search(str(value)))