import logging
from uuid import UUID

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .forms import AnswerForm
from .models import Challenge, Context, Level, LevelSequence, Question, User

# Get an instance of a logger
logger = logging.getLogger(__name__)


def find_user_by_uuid(user_uuid: UUID) -> User:
    """Get a user by its UUID."""
    try:
        return User.objects.get(uuid=user_uuid)
    except User.DoesNotExist as e:
        logger.error("User does not exist.")
        raise e


def set_next_level_user(request: HttpRequest, user: User) -> None:
    current_index = user.current_level.index
    next_level = Level.objects.filter(index__gt=current_index).order_by("index").first()

    if next_level:
        user.current_level = next_level
        first_level_position = user.current_level.get_first_level_position()
        if first_level_position:
            user.current_position = first_level_position
        else:
            user.current_position = None
        user.save()
    else:
        messages.success(
            request,
            _("Congratulations! You have completed all available levels.!"),
        )
        return HttpResponseRedirect("/dashboard")


def set_next_position_user(user: User) -> None:
    level_sequence = LevelSequence.objects.filter(level=user.current_level)

    if level_sequence:
        next_position = (
            level_sequence.filter(position__gt=user.current_position)
            .order_by("position")
            .first()
        )

        if next_position:
            user.current_position = next_position.position
            user.save()


def set_previous_position_user(user: User) -> None:
    level_sequence = LevelSequence.objects.filter(level=user.current_level)

    if level_sequence:
        previous_position = (
            level_sequence.filter(position__lt=user.current_position)
            .order_by("position")
            .last()
        )

        if previous_position:
            user.current_position = previous_position.position
            user.save()


def set_progress_course(user: User):
    level_sequence = LevelSequence.objects.filter(level=user.current_level)
    user_score = user.score_set.filter(level=user.current_level).first()

    if level_sequence:
        index = level_sequence.filter(position__lte=user.current_position).count()
        progress = index / level_sequence.count() * 100

    if user_score:
        user_score.progress = progress
        user_score.save()


def get_slides_content(user: User) -> []:
    slides = []
    level_sequence = LevelSequence.objects.filter(
        level=user.current_level, position__gte=user.current_position
    ).order_by("position")[:2]
    for sequence in level_sequence:
        content_type = sequence.content_type
        object_id = sequence.object_id

        if content_type == ContentType.objects.get_for_model(Context):
            context = get_object_or_404(Context, pk=object_id)
            slides.append(
                {
                    "context": {
                        "texts": context.contexttexttemplate_set.all(),
                        "medias": context.contextmediatemplate_set.all(),
                    }
                }
            )
        elif content_type == ContentType.objects.get_for_model(Question):
            question = get_object_or_404(Question, pk=object_id)
            form = AnswerForm(question=question)
            form.question_index = get_question_index(sequence.position)
            slides.append({"question": form})
        elif content_type == ContentType.objects.get_for_model(Challenge):
            challenge = get_object_or_404(Challenge, pk=object_id)
            slides.append({"challenge": challenge})

    return slides


def get_question_index(position: int) -> int:
    questions = LevelSequence.objects.filter(
        content_type=ContentType.objects.get_for_model(Question)
    )
    index = questions.filter(position__lt=position).count()
    return index


def set_status_carousel_controls(user: User) -> [bool, bool]:
    try:
        current_sequence = LevelSequence.objects.get(
            level=user.current_level, position=user.current_position
        )

        sequence_before = (
            LevelSequence.objects.filter(
                level=user.current_level, position__lt=user.current_position
            )
            .order_by("position")
            .last()
        )

        sequence_after = (
            LevelSequence.objects.filter(
                level=user.current_level, position__gt=user.current_position
            )
            .order_by("position")
            .first()
        )

        previous_control_enable = bool(
            sequence_before
            and sequence_before.content_type
            != ContentType.objects.get_for_model(Question)
        )
        next_control_enable = bool(
            sequence_after
            and current_sequence.content_type
            != ContentType.objects.get_for_model(Question)
        )

    except LevelSequence.DoesNotExist:
        previous_control_enable = False
        next_control_enable = False

    return [previous_control_enable, next_control_enable]
