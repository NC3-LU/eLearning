import io
import mimetypes
import os
import zipfile

from django.contrib import messages
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .decorators import user_uuid_required
from .forms import ResourceDownloadForm, inputUserUUIDForm
from .models import Category, Knowledge, Level, Resource, ResourceType, Score, User
from .settings import COOKIEBANNER
from .viewLogic import find_user_by_uuid


def index(request):
    request.session.clear()
    user_uuid_param = request.GET.get("user_uuid", None)
    if user_uuid_param:
        request.session["user_uuid"] = user_uuid_param
        return HttpResponseRedirect("/dashboard")

    levels = Level.objects.order_by("index")
    context = {
        "levels": levels,
    }
    return render(request, "landing.html", context=context)


def start(request):
    if request.method == "POST":
        form = inputUserUUIDForm(request.POST)
        if form.is_valid():
            user_uuid = form.cleaned_data["user_uuid"]
            request.session["user_uuid"] = str(user_uuid)
            return HttpResponseRedirect("/dashboard")
        else:
            messages.error(request, form.errors["user_uuid"])
            return HttpResponseRedirect("/")
    else:
        form = inputUserUUIDForm()
    return render(request, "modals/start.html", {"form": form})


def new_user(request):
    levels = Level.objects.order_by("index")
    categories = Category.objects.order_by("index")
    user = User()
    user.save()
    for level in levels:
        score = Score()
        score.user = user
        score.level = level
        score.save()

    for category in categories:
        knowledge = Knowledge()
        knowledge.user = user
        knowledge.category = category
        knowledge.save()

    request.session["user_uuid"] = str(user.uuid)
    return render(request, "modals/new_user.html")


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


@user_uuid_required
def dashboard(request):
    user_uuid = request.session.get("user_uuid")
    user = find_user_by_uuid(user_uuid)
    knowledge = Knowledge.objects.filter(user=user).order_by("category__index")
    scores = Score.objects.filter(user=user).order_by("level__index")

    criteria = {
        "labels": list(
            knowledge.values_list("category__translations__name", flat=True)
        ),
        "data": list(knowledge.values_list("progress", flat=True)),
    }
    progress_json = [
        {"index": score.level.index, "progress": score.progress} for score in scores
    ]

    context = {
        "user": user,
        "scores": scores,
        "progress_json": progress_json,
        "criteria": criteria,
    }
    return render(request, "dashboard.html", context=context)


@user_uuid_required
def course(request):
    return render(request, "course.html")


@user_uuid_required
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


@user_uuid_required
def resources_download(request):
    resource_type_id = request.GET.get("resource_type")
    level_id = request.GET.get("level")
    resources = Resource.objects.all().order_by("level", "resourceType")

    if resource_type_id:
        resources = resources.filter(resourceType=resource_type_id)

    if level_id:
        resources = resources.filter(level=level_id)

    ResourceFormSet = formset_factory(ResourceDownloadForm, extra=0)

    if request.method == "POST":
        formset = ResourceFormSet(
            request.POST,
            initial=[{"resource": resource} for resource in resources],
            prefix="resources",
        )
        if formset.is_valid():
            selected_resources_ids = []
            for index, _form in enumerate(formset):
                checkbox_name = f"resources-{index}-resource"
                if checkbox_name in request.POST:
                    selected_resources_ids.append(request.POST.get(checkbox_name))

        resources_selected = resources.filter(id__in=selected_resources_ids)

        if resources_selected.count() > 1:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for resource in resources_selected:
                    file_name_temp, file_extension = os.path.splitext(resource.path)
                    file_name = f"{resource.name}{file_extension}"
                    zip_file.write(resource.path, arcname=file_name)

            response = HttpResponse(
                zip_buffer.getvalue(), content_type="application/zip"
            )
            response["Content-Disposition"] = 'attachment; filename="resources.zip"'

        elif resources_selected.count() == 1:
            resource = resources_selected.first()
            content_type, _ = mimetypes.guess_type(resource.path)
            file_name_temp, file_extension = os.path.splitext(resource.path)
            file_name = f"{resource.name}{file_extension}"

            with open(resource.path, "rb") as file:
                response = HttpResponse(file.read(), content_type=content_type)
                response["Content-Disposition"] = f'attachment; filename="{file_name}"'

        else:
            return HttpResponseRedirect("/resources")

        return response

    else:
        formset = ResourceFormSet(
            initial=[{"resource": resource} for resource in resources],
            prefix="resources",
        )

    for form in formset:
        if form.resource_type.index == 1:
            form.icon_class = "text-warning"
        elif form.resource_type.index == 2:
            form.icon_class = "text-primary"
        elif form.resource_type.index == 3:
            form.icon_class = "text-blue-dark"

        if form.fields["resource"].disabled:
            form.icon_class = "text-secondary"

    return render(request, "modals/resources_download.html", {"formset": formset})
