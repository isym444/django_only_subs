from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def days_ago(value):
    if not value:
        return ""
    try:
        # Convert string to datetime if needed
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        
        # Calculate days difference
        delta = timezone.now() - value
        days = delta.days
        
        if days == 0:
            return "today"
        elif days == 1:
            return "yesterday"
        else:
            return f"{days} days ago"
    except:
        return "" 