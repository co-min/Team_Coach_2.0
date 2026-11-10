# Color Mapping

# function/hints.py

HINT_COLORS = {
    "low": "#FF1515",
    "medium": "#F3E221",
    "high": "#2BB830",
}


def get_hint_color(level: str) -> str:
    """Convert an attribute level to its display color."""
    return HINT_COLORS[level.lower()]