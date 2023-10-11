from django.shortcuts import render

from .models import Level, Resource, ResourceType
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


def dashboard(request):
    levels = Level.objects.order_by("index")
    for level in levels:
        # TODO: calculate the actual completion when it will be possible
        level.progress = f"{(5 - level.index) * 0.25:.0%}"
    context = {
        "levels": levels,
    }
    return render(request, "dashboard.html", context=context)


def course(request):
    return render(request, "course.html")


def resources(request):
    levels = Level.objects.order_by("index")
    resourcesType = ResourceType.objects.order_by("index")
    resources = Resource.objects.all()
    context = {
        "levels": levels,
        "resources": resources,
        "resourcesType": resourcesType,
    }

    return render(request, "resources.html", context=context)
