from __future__ import annotations
import json

# Color palette used by the Tkinter UI - Green theme
COLORS = {
	"background": "#f0fdf4",  # green-50 - light green background
	"text_primary": "#166534",  # green-800 - dark green text
	"text_secondary": "#16a34a",  # green-600 - medium green text
	"primary": "#22c55e",  # green-500 - bright green
	"secondary": "#84cc16",  # lime-500 - lime green
	"accent": "#10b981",  # emerald-500 - emerald green
	"border": "#bbf7d0",  # green-200 - light green border
    "card_bg": "#FFFFFF",      # White
    "success": "#10B981",      # Green
    "warning": "#F59F0B",      # Yellow
    "error": "#EF4444",        # Red
}

def safe_json_loads(json_string, default=None):
    """Safely load JSON from string with error handling"""
    if json_string is None:
        return default
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(data, default=None):
    """Safely dump data to JSON string with error handling"""
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return default

def format_time_delta(delta):
    """Format timedelta to human readable string"""
    if delta.days > 0:
        return f"{delta.days} days"
    elif delta.seconds >= 3600:
        hours = delta.seconds // 3600
        return f"{hours} hours"
    elif delta.seconds >= 60:
        minutes = delta.seconds // 60
        return f"{minutes} minutes"
    else:
        return f"{delta.seconds} seconds"

def get_current_timestamp():
    """Get current timestamp in ISO format"""
    from datetime import datetime
    return datetime.now().isoformat()

