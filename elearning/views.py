from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def course(request):
    return render(request, "course.html")
