from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_otp.decorators import otp_required
from .forms import PreliminaryNotificationForm
from django.http import HttpResponseRedirect

from nisinp.settings import SITE_NAME

@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        return redirect("admin:index")

def logout_view(request):
    logout(request)
    return redirect("login")


def terms(request):
    return render(request, "home/terms.html", context={"site_name": SITE_NAME})


def privacy(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})

def index(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})

def notifications(request):
    return render(request, "notification/index.html", context={"site_name": SITE_NAME})

def declaration(request):
    form = PreliminaryNotificationForm()
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PreliminaryNotificationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("incident_list")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PreliminaryNotificationForm()

    return render(request, "notification/declaration.html", context={"site_name": SITE_NAME, "form": form})

def incident_list(request):
    return render(request, "notification/incident_list.html", context={"site_name": SITE_NAME})