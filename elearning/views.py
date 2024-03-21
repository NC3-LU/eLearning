import io
import mimetypes
import os
import zipfile

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, BooleanField, Case, Count, F, Value, When
from django.db.models.query import QuerySet
from django.forms.formsets import formset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .decorators import user_uuid_required
from .forms import AnswerForm, ResourceDownloadForm, inputUserUUIDForm
from .models import (
    Answer,
    AnswerChoice,
    Category,
    Knowledge,
    Level,
    LevelSequence,
    Question,
    Resource,
    ResourceType,
    Score,
    User,
)
from .settings import COOKIEBANNER
from .viewLogic import (
    get_allowed_resources_ids,
    get_questions_success_rate,
    get_quiz_order,
    get_report_pdf,
    get_slides_content,
    get_user_from_request,
    set_knowledge_course,
    set_next_level_user,
    set_position_user,
    set_progress_course,
    set_score_course,
    set_status_carousel_controls,
)


def index(request):
    request.session.flush()
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
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            messages.error(request, form.errors["user_uuid"])
            return HttpResponseRedirect(reverse("index"))
    else:
        form = inputUserUUIDForm()
    return render(request, "modals/start.html", {"form": form})


def new_user(request):
    levels = Level.objects.order_by("index")
    categories = Category.objects.order_by("index")
    first_level = Level.objects.order_by("index").first()

    user = User()

    if first_level:
        user.current_level = first_level

    user.save()

    for level in levels:
        score = Score(user=user, level=level)
        score.save()

    for category in categories:
        knowledge = Knowledge(user=user, category=category)
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


def helping_center(request):
    return render(request, "helping_center.html")


def accessibility(request):
    return render(request, "accessibility.html")


def stats(request):
    questions_success_rate = list(get_questions_success_rate())
    global_total_users = User.objects.all().count()
    global_avg_score = Score.objects.aggregate(avg_score=Avg("score"))["avg_score"]
    avg_score_by_level = list(
        Score.objects.values("level__translations__name", "level__index")
        .annotate(avg_score=Avg("score"))
        .order_by("level__index")
    )
    avg_progress_by_level = list(
        Score.objects.values("level__index")
        .annotate(avg_progress=Avg("progress"))
        .order_by("level__index")
    )
    users_by_date = list(
        User.objects.values("created_at")
        .annotate(timestamp=F("created_at"), count=Count("id"))
        .order_by("created_at")
        .values("timestamp", "count")
    )
    users_by_level = list(
        User.objects.values("current_level__translations__name", "current_level__index")
        .order_by("current_level__index")
        .annotate(
            level_index=F("current_level__index"),
            level_name=F("current_level__translations__name"),
            count=Count("id"),
        )
        .values("level_index", "level_name", "count")
    )
    users_current_position = list(
        User.objects.exclude(current_position=None)
        .values(
            "current_level__translations__name",
            "current_level__index",
            "current_position",
        )
        .annotate(total_users=Count("id"))
        .order_by("-total_users")
    )
    context = {
        "questions_success_rate": questions_success_rate,
        "global_total_users": global_total_users,
        "global_avg_score": global_avg_score,
        "avg_score_by_level": avg_score_by_level,
        "avg_progress_by_level": avg_progress_by_level,
        "users_by_date": users_by_date,
        "users_by_level": users_by_level,
        "users_current_position": users_current_position,
    }

    return render(request, "stats.html", context=context)


@user_uuid_required
def dashboard(request):
    user = get_user_from_request(request)
    knowledge = Knowledge.objects.filter(user=user).order_by("category__index")
    scores = Score.objects.filter(user=user).order_by("level__index")
    criteria = {
        "data": [
            {"label": label, "value": progress}
            for label, progress in zip(
                knowledge.values_list("category__translations__name", flat=True),
                knowledge.values_list("progress", flat=True),
            )
        ]
    }

    progress = list(scores.values_list("progress", flat=True))
    success = list(scores.values_list("score", flat=True))

    context = {
        "user": user,
        "scores": scores,
        "success": success,
        "progress": progress,
        "criteria": criteria,
    }

    return render(request, "dashboard.html", context=context)


@user_uuid_required
def course(request):
    user = get_user_from_request(request)

    if user.get_level_progress() == 100:
        set_next_level_user(request, user)

    if not user.current_position:
        first_level_position = user.current_level.get_first_level_position()
        if first_level_position:
            user.current_position = first_level_position
            user.save()

    if user.current_level and user.current_position:
        if request.method == "POST":
            level_sequence = LevelSequence.objects.get(
                level=user.current_level, position=user.current_position
            )
            if level_sequence.content_type == ContentType.objects.get_for_model(
                Question
            ):
                question = level_sequence.content_object
                form = AnswerForm(request.POST, question=question, user=user)
                if form.is_valid():
                    existing_answer = Answer.objects.filter(
                        user=user, question=question
                    )
                    if not existing_answer:
                        set_knowledge_course(user, question)
                        user_answer_choices = form.cleaned_data["answer"]
                        answer = Answer(user=user, question=question)
                        answer.save()
                        if not isinstance(user_answer_choices, QuerySet):
                            user_answer_choices = [user_answer_choices]

                        if question.q_type == "SR":
                            user_answer_choices = form.data.getlist("answer")
                            for user_answer in form.data.getlist("answer"):
                                choice = AnswerChoice.objects.get(id=user_answer)
                                answer.answer_choices.add(choice)
                        else:
                            answer.answer_choices.set(user_answer_choices, clear=True)

                        set_score_course(user, question, user_answer_choices)

                    return JsonResponse({"success": True})

            return JsonResponse({"success": False})

        slides = get_slides_content(user, None)
    else:
        messages.warning(request, _("No data available to start the level"))
        return HttpResponseRedirect(reverse("dashboard"))

    [previous_control_enable, next_control_enable] = set_status_carousel_controls(user)

    context = {
        "previous_control_enable": previous_control_enable,
        "next_control_enable": next_control_enable,
        "progress": user.score_set.get(level=user.current_level).progress,
        "quizzes": get_quiz_order(user),
        "level": user.current_level,
        "score": user.score_set.get(level=user.current_level).score,
        "slides": slides,
    }

    return render(request, "course.html", context=context)


@user_uuid_required
def update_progress_bar(request):
    user = get_user_from_request(request)
    direction = request.GET.get("direction", None)
    if user.current_level and user.current_position:
        set_position_user(user, direction=direction)
        quizzes = get_quiz_order(user)
        set_progress_course(user, quizzes)
    context = {
        "progress": user.score_set.get(level=user.current_level).progress,
        "quizzes": quizzes,
    }
    return render(request, "parts/course_progress_bar.html", context=context)


@user_uuid_required
def change_slide(request):
    user = get_user_from_request(request)
    direction = request.GET.get("direction", None)

    if user.current_level and user.current_position:
        slides = get_slides_content(user, direction=direction)
    else:
        messages.warning(request, _("No data available to start the level"))
        return HttpResponseRedirect(reverse("dashboard"))

    context = {
        "slide": slides[0] if slides else None,
        "level": user.current_level,
        "score": user.score_set.get(level=user.current_level).score,
    }

    return render(request, "course_new_slide.html", context=context)


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
    user = get_user_from_request(request)
    resource_type_id = request.GET.get("resource_type")
    level_id = request.GET.get("level")
    resources = Resource.objects.all().order_by("level", "resourceType")

    if resource_type_id:
        resources = resources.filter(resourceType=resource_type_id)

    if level_id:
        resources = resources.filter(level=level_id)

    allowed_resources_ids = get_allowed_resources_ids(user)

    resources = resources.annotate(
        disabled=Case(
            When(id__in=allowed_resources_ids, then=Value(False)),
            default=Value(True),
            output_field=BooleanField(),
        )
    )

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
            return HttpResponseRedirect(reverse("resources"))

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


@user_uuid_required
def report(request):
    user = get_user_from_request(request)

    if not user.get_level_progress() >= 100:
        return HttpResponseRedirect(reverse("dashboard"))

    pdf_report = get_report_pdf(user, request)

    # Return the report in the HTTP answer
    response = HttpResponse(pdf_report, content_type="application/pdf")
    response["Content-Disposition"] = "attachment;filename=Report.pdf"

    return response
