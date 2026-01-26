from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies the value by the argument."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''
    
@register.filter
def duration_hours(value):
    """
    Extract hours from a DurationField.
    """
    if value:
        total_seconds = value.total_seconds()
        hours = int(total_seconds // 3600)  
        return f"{hours} h"
    return "0 h"