"""
URL configuration for E-learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.views.i18n import set_language

from elearning import views

from .admin import admin_site
from .settings import DEBUG

urlpatterns = [
    # Root
    path("", views.index, name="index"),
    # Admin
    path("admin/", admin_site.urls),
    # Language Selector
    path("set-language/", set_language, name="set_language"),
    #   Start Modal
    path("start/", views.start, name="start"),
    #   New User Modal
    path("new_user/", views.new_user, name="new_user"),
    # Privacy Policy
    path("privacy/", views.privacy_policy, name="privacy"),
    # Cookies
    path("cookies/", views.cookies, name="cookies"),
    # Terms of Service
    path("tos/", views.tos, name="tos"),
    # Legal
    path("legal/", views.legal, name="legal"),
    # Help
    path("helping_center", views.helping_center, name="helping_center"),
    # Accessibility
    path("accessibility/", views.accessibility, name="accessibility"),
    # Dashboard
    path("dashboard", views.dashboard, name="dashboard"),
    # Course
    path("course", views.course, name="course"),
    path("change_slide/", views.change_slide, name="change_slide"),
    path("update_progress_bar/", views.update_progress_bar, name="update_progress_bar"),
    #   Resources
    path("resources", views.resources, name="resources"),
    #   ResourcesDownload Modal
    path("resources_download/", views.resources_download, name="resources_download"),
    #   Report Download
    path("report/", views.report, name="report"),
]

if DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
