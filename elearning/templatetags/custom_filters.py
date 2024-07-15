import os

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def is_sticker_unlocked(score):
    if score == 0:
        return "1"
    if score < 70:
        return "2"
    if score >= 70 and score < 90:
        return "3"
    if score >= 90:
        return "4"


@register.filter(name="split")
def split(value, key):
    return value.split(key)


@register.filter(name="extract_static")
def extract_static_part(file_path):
    return os.path.relpath(file_path, settings.STATIC_THEME_DIR)


@register.filter(name="starts_with")
def starts_with(value, arg):
    return value.startswith(arg)


@register.filter(name="contains")
def contains(value, arg):
    return arg in value


@register.simple_tag
def filter_by_value(obj_list, key, value):
    return [obj for obj in obj_list if getattr(obj, key) == value]


@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f"{days}d " if days else ""
    hours_str = f"{hours}h " if hours else ""
    minutes_str = f"{minutes}m " if minutes else ""
    seconds_str = f"{seconds}s" if seconds and not hours_str else ""

    return f"{days_str}{hours_str}{minutes_str}{seconds_str}"


@register.filter
def accumulate_quiz_index(value, arg):
    try:
        return (int(value) * 4 - 4) + int(arg)
    except (ValueError, TypeError):
        return ""


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
