from django import template

register = template.Library()


@register.filter
def is_sticker_unlocked(level, sticker):
    if level.progress == "100%":
        if sticker == "1":
            return True
        elif sticker == "2" and level.score >= 70:
            return True
        elif sticker == "3" and level.score > 80:
            return True
    return False
