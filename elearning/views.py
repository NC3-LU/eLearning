import io
import mimetypes
import os
import zipfile

from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import ResourceDownloadForm
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
    levels = Level.objects.all().order_by("index")
    # TODO: Get criteria values from querysets
    criteria = {
        "labels": [
            "Procédures",
            "Formation",
            "Traitement",
            "Sous-traitance",
            "Information",
            "Risques",
            "Violation de données",
            "Documentation",
            "Transfers",
        ],
        "data": [1, 0, 0.33, 0.5, 0.2, 0.3, 0.1, 0.15, 0.6],
    }
    levels_json = []
    for level in levels:
        # TODO: calculate the actual completion when it will be possible
        # level.progress = f"{4 * 0.25:.0%}"
        level.progress = f"{(5 - level.index) * 0.25:.0%}"
        # level.score = 80
        level.score = (5 - level.index) * 20
        levels_json.append(
            {
                "id": level.id,
                "index": level.index,
                "name": level.name,
                "description": level.description,
                "progress": (5 - level.index) * 25,
            }
        )

    context = {
        "levels": levels,
        "levels_json": levels_json,
        "criteria": criteria,
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
