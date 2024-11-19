"""Configuration settings for the Cultural Map application."""

# Page configuration
PAGE_CONFIG = {
    "page_title": "Carte Culturelle de France",
    "page_icon": "🎭",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Map configuration
MAP_CONFIG = {
    "FRANCE_CENTER": (46.603354, 1.888334),
    "FRANCE_SW": (41.333, -4.833),
    "FRANCE_NE": (51.2, 9.833),
    "DEFAULT_ZOOM": 6,
    "MIN_ZOOM": 6,
    "MAX_ZOOM": 18
}

# Category colors
CATEGORY_COLORS = {
    "patrimoine": "blue",
    "spectacle_vivant": "red"
}
