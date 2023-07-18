from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_otp.decorators import otp_required

from nisinp.settings import SITE_NAME

@login_required
def index(request):
    if not request.user.is_verified():
        return redirect("two_factor:profile")

    otp_required(index)

    user = request.user
    if user.is_authenticated:
        if user.is_operateur:
            return index(request)
        elif user.is_regulator:
            return index(request)


def logout_view(request):
    logout(request)
    return redirect("login")


def terms(request):
    return render(request, "home/terms.html", context={"site_name": SITE_NAME})


def privacy(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})

def index(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})