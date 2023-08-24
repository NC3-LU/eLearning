from django.shortcuts import render

from .models import Level, Resource


def index(request):
    return render(request, "index.html")


def course(request):
    context = {
        "levels": Level.objects.order_by("index"),
    }
    return render(request, "course.html", context=context)


def resources(request):
    context = {
        "resources": Resource.objects.order_by("level"),
    }
    return render(request, "resources.html", context=context)
