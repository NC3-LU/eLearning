from django.shortcuts import render

from .models import Level, Resource
from .settings import COOKIEBANNER


def index(request):
    levels = Level.objects.order_by("index")
    for level in levels:
        level.description_lines = level.description.split("\n")
    context = {
        "levels": levels,
    }
    return render(request, "landing.html", context=context)


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def cookies(request):
    return render(request, "cookies.html", context=COOKIEBANNER)


def tos(request):
    return render(request, "tos.html")


def legal(request):
    return render(request, "legal.html")


def accessibility(request):
    return render(request, "accessibility.html")


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
