import os

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def is_sticker_unlocked(score, sticker):
    if score.progress == 100:
        if sticker == "1":
            return True
        elif sticker == "2" and score.score >= 70:
            return True
        elif sticker == "3" and score.score > 90:
            return True
    return False


@register.filter(name="split")
def split(value, key):
    return value.split(key)


@register.filter(name="extract_static")
def extract_static_part(file_path):
    return os.path.relpath(file_path, settings.STATIC_THEME_DIR)
