from django import template

register = template.Library()


@register.inclusion_tag("components/course_question_multiple_choice.html")
def multiple_choice_question(value):
    return {"value": value}


@register.inclusion_tag("components/course_question_single_choice.html")
def single_choice_question(value):
    return {"value": value}
