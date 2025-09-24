from django import template
import re
register = template.Library()

@register.simple_tag
def render_stars(rating, max_stars=5, filled_star='★', half_star='½', empty_star='☆'):
    """Render a star bar with optional half star.

    Accepts int or float rating. Rounds to nearest 0.5.
    Example:
      4.3 -> ★★★★½☆
      4.74 -> ★★★★★
      0.2 -> ½☆☆☆☆

    Parameters:
      rating (int|float|str): The numeric rating (0..max_stars). Non-numeric -> 0.
      max_stars (int): Total star slots.
      filled_star (str): Glyph for a full star.
      half_star (str): Glyph for a half star (text fallback). Swap for a custom span if desired.
      empty_star (str): Glyph for an empty star.
    """
    try:
        value = float(rating)
    except (TypeError, ValueError):
        value = 0.0
    if value < 0:
        value = 0.0
    if value > max_stars:
        value = float(max_stars)

    # Round to nearest half step
    halves = round(value * 2) / 2.0  # e.g. 4.26 -> 4.5, 4.74 -> 4.5 (Python bankers rounding is fine here)
    full = int(halves)
    has_half = 1 if (halves - full) == 0.5 else 0
    empty = max_stars - full - has_half

    return (filled_star * full) + (half_star if has_half else '') + (empty_star * empty)

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