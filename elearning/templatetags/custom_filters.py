from django import template

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


@register.inclusion_tag("parts/course_progress_bar.html")
def course_progress_bar(value):
    value = max(0, min(value, 100))
    return {"value": value}
