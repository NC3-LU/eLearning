from django import template

register = template.Library()


@register.filter
def is_sticker_unlocked(score, sticker):
    if score.progress == 1:
        if sticker == "1":
            return True
        elif sticker == "2" and score.score >= 0.70:
            return True
        elif sticker == "3" and score.score > 0.90:
            return True
    return False


@register.filter(name="split")
def split(value, key):
    return value.split(key)
