import io
import mimetypes
import os
import zipfile
from decimal import Decimal

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    Avg,
    BooleanField,
    Case,
    Count,
    DurationField,
    ExpressionWrapper,
    F,
    Q,
    Value,
    When,
)
from django.db.models.query import QuerySet
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .decorators import handle_template_not_found, user_uuid_required
from .forms import AnswerForm, ResourceDownloadForm, inputUserUUIDForm
from .models import (
    Answer,
    AnswerChoice,
    Category,
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


@handle_template_not_found
def index(request):
    request.session.flush()
    change_sidebar_state(request)
    user_uuid_param = request.GET.get("user_uuid", None)
    if user_uuid_param:
        request.session["user_uuid"] = user_uuid_param
        return HttpResponseRedirect("/dashboard")
    levels = Level.objects.order_by("index")
    context = {
        "levels": levels,
    }
    return render(request, "landing.html", context=context)


@handle_template_not_found
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


@handle_template_not_found
def change_sidebar_state(request):
    state = request.GET.get("state", "expanded")
    request.session["sidebar_state"] = state
    return JsonResponse({"state": state})


@handle_template_not_found
def new_user(request):
    first_level = Level.objects.order_by("index").first()

    user = User()

    if first_level:
        user.current_level = first_level

    user.save()

    request.session["user_uuid"] = str(user.uuid)
    return render(request, "modals/new_user.html")


@handle_template_not_found
def privacy_policy(request):
    return render(request, "privacy_policy.html")


@handle_template_not_found
def cookies(request):
    return render(request, "cookies.html", context=COOKIEBANNER)


@handle_template_not_found
def tos(request):
    return render(request, "tos.html")


@handle_template_not_found
def legal(request):
    return render(request, "legal.html")


@handle_template_not_found
def helping_center(request):
    return render(request, "helping_center.html")


@handle_template_not_found
def accessibility(request):
    return render(request, "accessibility.html")


@handle_template_not_found
def stats(request):
    users_qs = User.objects.filter(
        current_level__translations__language_code=request.LANGUAGE_CODE
    )
    score_qs = Score.objects.filter(
        level__translations__language_code=request.LANGUAGE_CODE
    )
    questions_success_rate = list(get_questions_success_rate())
    global_total_users = users_qs.count()
    global_avg_score = score_qs.aggregate(avg_score=Avg("score"))["avg_score"]
    avg_score_and_progress_by_level = list(
        score_qs.values("level__translations__name", "level__index")
        .order_by("level__index")
        .annotate(
            level_index=F("level__index"),
            level_name=F("level__translations__name"),
            count=Count("id"),
            avg_score=Avg("score"),
            avg_progress=Avg("progress"),
        )
        .values("level_index", "level_name", "avg_score", "avg_progress", "count")
    )
    first_level = Level.objects.order_by("index").first()

    users_by_date = list(
        users_qs.annotate(
            is_unstarted=Case(
                When(
                    current_level=first_level,
                    current_position__isnull=True,
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            timestamp=F("created_at"),
        )
        .values("timestamp", "is_unstarted")
        .annotate(count=Count("id"))
        .order_by("timestamp")
        .values("timestamp", "is_unstarted", "count")
    )

    users_by_level = list(
        users_qs.exclude(current_level=first_level, current_position__isnull=True)
        .values("current_level", "current_level__index")
        .order_by("current_level__index")
        .annotate(
            level_index=F("current_level__index"),
            level_name=F("current_level__translations__name"),
            count=Count("id"),
        )
        .values("level_index", "level_name", "count")
    )
    users_current_position = list(
        users_qs.exclude(current_position__isnull=True)
        .values(
            "current_level__translations__name",
            "current_level__index",
            "current_position",
        )
        .annotate(total_users=Count("id"))
        .order_by("-total_users")
    )
    average_duration_by_level = list(
        score_qs.values("level__translations__name", "level__index")
        .order_by("level__index")
        .annotate(
            level_index=F("level__index"),
            level_name=F("level__translations__name"),
            duration_seconds=ExpressionWrapper(
                F("updated_at") - F("created_at"), output_field=DurationField()
            ),
        )
        .values("level_index", "level_name")
        .annotate(
            avg_duration=Avg(
                ExpressionWrapper(F("duration_seconds"), output_field=DurationField())
            )
        )
    )
    for field in average_duration_by_level:
        field["avg_duration"] = field["avg_duration"].total_seconds()

    global_avg_duration = score_qs.aggregate(
        global_avg_duration=Avg(
            ExpressionWrapper(
                F("updated_at") - F("created_at"), output_field=DurationField()
            )
        )
    )["global_avg_duration"]

    context = {
        "questions_success_rate": questions_success_rate,
        "global_total_users": global_total_users,
        "global_avg_score": global_avg_score,
        "global_avg_duration": global_avg_duration,
        "avg_score_and_progress_by_level": avg_score_and_progress_by_level,
        "users_by_date": users_by_date,
        "users_by_level": users_by_level,
        "users_current_position": users_current_position,
        "average_duration_by_level": average_duration_by_level,
    }

    return render(request, "stats.html", context=context)


@handle_template_not_found
@user_uuid_required
def dashboard(request):
    user = get_user_from_request(request)
    levels = Level.objects.all().order_by("index")
    categories = Category.objects.all().order_by("index")
    levels_by_score = {}
    knowledge = {}
    progress = []
    success = []

    for level in levels:
        score = level.score_set.filter(Q(user=user) | Q(user=None)).first()
        levels_by_score[level] = score
        progress.append(score.progress if score else Decimal(0))
        success.append(score.score if score else Decimal(0))

    for category in categories:
        knowledge[category] = category.knowledge_set.filter(
            Q(user=user) | Q(user=None)
        ).first()

    context = {
        "user": user,
        "success": success,
        "progress": progress,
        "levels": levels_by_score,
        "knowledge": knowledge,
    }

    return render(request, "dashboard.html", context=context)


@handle_template_not_found
@user_uuid_required
def course(request):
    user = get_user_from_request(request)
    level_id = request.GET.get("level", None)

    if level_id is not None:
        try:
            level_id = int(level_id)
        except ValueError:
            raise Http404

        if level_id < user.current_level.id:
            try:
                level_reviewed = Level.objects.get(id=level_id)
            except Level.DoesNotExist:
                raise Http404

            level_reviewed_cookie = request.session.get("level_reviewed")
            if not level_reviewed_cookie or level_reviewed_cookie != level_id:
                request.session["level_reviewed"] = level_reviewed.id
                request.session[
                    "level_reviewed_position"
                ] = level_reviewed.get_first_level_position()

            position_level_reviewed = request.session.get("level_reviewed_position")
            slides = get_slides_content(
                user, level_reviewed, position_level_reviewed, None
            )
            previous_control_enable, next_control_enable = set_status_carousel_controls(
                level_reviewed, position_level_reviewed
            )

            user_score = user.score_set.get(level=level_reviewed)

            context = {
                "previous_control_enable": previous_control_enable,
                "next_control_enable": next_control_enable,
                "progress": user_score.progress,
                "quizzes": get_quiz_order(level_reviewed),
                "level": level_reviewed,
                "score": user_score.score,
                "slides": slides,
            }

            return render(request, "course.html", context=context)

    if "level_reviewed" in request.session:
        del request.session["level_reviewed"]
        del request.session["level_reviewed_position"]

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

        slides = get_slides_content(
            user, user.current_level, user.current_position, None
        )
    else:
        messages.warning(request, _("No data available to start the level"))
        return HttpResponseRedirect(reverse("dashboard"))

    [previous_control_enable, next_control_enable] = set_status_carousel_controls(
        user.current_level, user.current_position
    )

    user_score, _created = Score.objects.get_or_create(
        user=user,
        level=user.current_level,
    )

    context = {
        "previous_control_enable": previous_control_enable,
        "next_control_enable": next_control_enable,
        "progress": user_score.progress,
        "quizzes": get_quiz_order(user.current_level),
        "level": user.current_level,
        "score": user_score.score,
        "slides": slides,
    }

    return render(request, "course.html", context=context)


@handle_template_not_found
@user_uuid_required
def update_progress_bar(request):
    user = get_user_from_request(request)
    direction = request.GET.get("direction", None)
    level_reviewed_cookie = request.session.get("level_reviewed")
    position_level_reviewed = request.session.get("level_reviewed_position")

    if level_reviewed_cookie and position_level_reviewed:
        try:
            user_level = Level.objects.get(id=level_reviewed_cookie)
        except Level.DoesNotExist:
            raise Http404

        set_position_user(
            request, user, user_level, position_level_reviewed, direction=direction
        )
        quizzes = get_quiz_order(user_level)
    elif user.current_level and user.current_position:
        set_position_user(
            request,
            user,
            user.current_level,
            user.current_position,
            direction=direction,
        )
        quizzes = get_quiz_order(user.current_level)
        set_progress_course(user, quizzes)
        user_level = user.current_level

    try:
        progress = user.score_set.get(level=user_level).progress
    except Score.DoesNotExist:
        progress = 0

    context = {
        "progress": progress,
        "quizzes": quizzes,
    }
    return render(request, "parts/course_progress_bar.html", context=context)


@handle_template_not_found
@user_uuid_required
def change_slide(request):
    user = get_user_from_request(request)
    direction = request.GET.get("direction", None)
    level_reviewed_cookie = request.session.get("level_reviewed")
    position_level_reviewed = request.session.get("level_reviewed_position")

    if level_reviewed_cookie and position_level_reviewed:
        try:
            user_level = Level.objects.get(id=level_reviewed_cookie)
            user_position = position_level_reviewed
        except Level.DoesNotExist:
            raise Http404

    elif user.current_level and user.current_position:
        user_level = user.current_level
        user_position = user.current_position
    else:
        messages.warning(request, _("No data available to start the level"))
        return HttpResponseRedirect(reverse("dashboard"))

    slides = get_slides_content(user, user_level, user_position, direction=direction)

    context = {
        "slide": slides[0] if slides else None,
        "level": user_level,
        "score": user.score_set.get(level=user_level).score,
    }

    return render(request, "course_new_slide.html", context=context)


@handle_template_not_found
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


@handle_template_not_found
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
    level_reviewed_cookie = request.session.get("level_reviewed")

    if level_reviewed_cookie:
        try:
            user_level = Level.objects.get(id=level_reviewed_cookie)
        except Level.DoesNotExist:
            raise Http404
    elif not user.get_level_progress() >= 100:
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        user_level = user.current_level

    pdf_report = get_report_pdf(request, user, user_level)

    response = HttpResponse(pdf_report, content_type="application/pdf")
    response["Content-Disposition"] = "attachment;filename=Report.pdf"

    return response
