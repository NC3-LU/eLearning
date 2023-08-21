from django.shortcuts import render

from .models import Level


def index(request):
    return render(request, "index.html")


def course(request):
    context = {
        "levels": Level.objects.all(),
    }
    return render(request, "course.html", context=context)
