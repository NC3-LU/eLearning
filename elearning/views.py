from django.shortcuts import render

from .models import Level, Resource


def index(request):
    levels = Level.objects.order_by("index")
    for level in levels:
        level.description_lines = level.description.split("\n")
    context = {
        "levels": levels,
    }
    return render(request, "index.html", context=context)


def course(request):
    levels = Level.objects.order_by("index")
    for level in levels:
        level.description_lines = level.description.split("\n")
        # TODO: calculate the actual completion when it will be possible
        level.completion = (5 - level.id) * 25
    context = {
        "levels": levels,
    }
    return render(request, "course.html", context=context)


def resources(request):
    context = {
        "resources": Resource.objects.order_by("level__index", "category__index"),
    }
    return render(request, "resources.html", context=context)
