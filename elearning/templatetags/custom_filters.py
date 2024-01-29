import os

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def is_sticker_unlocked(score):
    if score.score == 0:
        return "1"
    if score.score < 70:
        return "2"
    if score.score >= 70 and score.score < 90:
        return "3"
    if score.score > 90:
        return "4"


@register.filter(name="split")
def split(value, key):
    return value.split(key)


@register.filter(name="extract_static")
def extract_static_part(file_path):
    return os.path.relpath(file_path, settings.STATIC_THEME_DIR)
