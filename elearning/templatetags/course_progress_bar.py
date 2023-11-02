from django import template

register = template.Library()


@register.inclusion_tag("components/course_progress_bar.html")
def course_progress_bar(value):
    value = max(0, min(value, 100))
    return {"value": value}
