from collections import Counter
from uuid import UUID

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .forms import AnswerForm
from .models import (
    AnswerChoice,
    Challenge,
    Context,
    Explanation,
    Knowledge,
    Level,
    LevelSequence,
    Question,
    Score,
    User,
)


def find_user_by_uuid(user_uuid: UUID) -> User:
    return get_object_or_404(User, uuid=user_uuid)


def get_user_from_request(request: HttpRequest) -> User:
    user_uuid = request.session["user_uuid"]
    user = find_user_by_uuid(user_uuid)
    return user


def set_next_level_user(request: HttpRequest, user: User) -> None:
    current_index = user.current_level.index
    next_level = Level.objects.filter(index__gt=current_index).order_by("index").first()

    if not next_level:
        messages.success(
            request,
            _("Congratulations! You have completed all available levels."),
        )
        return HttpResponseRedirect(reverse("dashboard"))

    user.current_level = next_level
    first_level_position = user.current_level.get_first_level_position()
    user.current_position = first_level_position if first_level_position else None
    user.save()


def set_position_user(user: User, direction: str) -> None:
    level_sequence = LevelSequence.objects.filter(level=user.current_level)

    if not level_sequence:
        return

    order_by_field = "position" if direction == "next" else "-position"
    filter_condition = "gt" if direction == "next" else "lt"

    position = (
        level_sequence.filter(
            **{f"position__{filter_condition}": user.current_position}
        )
        .order_by(order_by_field)
        .first()
    )

    if position:
        user.current_position = position.position
        user.save()


def set_progress_course(user: User) -> None:
    level_sequence = LevelSequence.objects.filter(level=user.current_level)
    user_score = user.score_set.filter(level=user.current_level).first()

    if not level_sequence or not user_score:
        return

    index = level_sequence.filter(position__lte=user.current_position).count()
    total_positions = level_sequence.count()

    if total_positions > 0:
        progress = (index / total_positions) * 100
        user_score.progress = progress
        user_score.save()


def set_knowledge_course(user: User, question: Question) -> None:
    question_contentType = ContentType.objects.get_for_model(Question)

    level_sequences_questions_all = LevelSequence.objects.filter(
        content_type=question_contentType
    )

    object_ids_all = level_sequences_questions_all.values_list("object_id", flat=True)

    questions_all = Question.objects.filter(id__in=object_ids_all)

    all_category_counts = Counter(
        questions_all.values_list("categories__id", flat=True)
    )

    for category in question.categories.all():
        knowledge = Knowledge.objects.get(user=user, category=category)
        total_category_count = all_category_counts[category.id]
        knowledge.save()
        percentage = (1 / total_category_count) * 100 if total_category_count > 0 else 0

        knowledge.progress = F("progress") + percentage
        knowledge.save()


def set_score_course(
    user: User, question: Question, user_answer_choices: AnswerChoice
) -> None:
    question_contentType = ContentType.objects.get_for_model(Question)

    level_sequences_questions_all = LevelSequence.objects.filter(
        content_type=question_contentType,
        level=user.current_level,
    )

    object_ids_all = level_sequences_questions_all.values_list("object_id", flat=True)

    total_correct_choices = Question.objects.filter(
        id__in=object_ids_all, answer_choices__is_correct=True
    ).count()

    if question.q_type == "SR":
        user_answers_are_correct = sum(
            x == str(y)
            for x, y in zip(
                user_answer_choices,
                question.answer_choices.order_by("index").values_list("id", flat=True),
            )
        )
    else:
        user_answers_are_correct = Counter(
            answer.is_correct for answer in user_answer_choices
        )[True]

    user_score = Score.objects.get(user=user, level=user.current_level)
    percentage = (
        (user_answers_are_correct / total_correct_choices) * 100
        if total_correct_choices > 0
        else 0
    )

    user_score.score = F("score") + percentage
    user_score.save()


def get_slides_content(user: User, direction: str) -> []:
    slides = []
    if not direction:
        level_sequence = LevelSequence.objects.filter(
            Q(level=user.current_level, position=user.current_position - 1)
            | Q(level=user.current_level, position=user.current_position)
            | Q(level=user.current_level, position=user.current_position + 1)
        ).order_by("position")
    elif direction == "next":
        level_sequence = LevelSequence.objects.filter(
            Q(level=user.current_level, position=user.current_position + 1)
        ).order_by("position")
    else:
        level_sequence = LevelSequence.objects.filter(
            Q(level=user.current_level, position=user.current_position - 1)
        ).order_by("position")

    for sequence in level_sequence:
        content_type = sequence.content_type
        object_id = sequence.object_id

        if content_type == ContentType.objects.get_for_model(Context):
            context = get_object_or_404(Context, pk=object_id)
            slides.append(
                {
                    "context": {
                        "texts": context.contexttexttemplate_set.all().order_by(
                            "index"
                        ),
                        "medias": context.contextmediatemplate_set.all(),
                    }
                }
            )
        elif content_type == ContentType.objects.get_for_model(Question):
            question = get_object_or_404(Question, pk=object_id)
            form = AnswerForm(question=question, user=user)
            form.question_index = get_question_index(user, sequence.position)
            slides.append({"question": form})
        elif content_type == ContentType.objects.get_for_model(Explanation):
            explanation = get_object_or_404(Explanation, pk=object_id)
            question_sequence = LevelSequence.objects.get(
                level=user.current_level, object_id=explanation.question.pk
            )
            slides.append(
                {
                    "explanation": {
                        "question": explanation.question,
                        "question_index": get_question_index(
                            user, question_sequence.position
                        ),
                        "label": explanation.name,
                        "texts": explanation.explanationtexttemplate_set.all(),
                        "medias": explanation.explanationmediatemplate_set.all(),
                    }
                }
            )
        elif content_type == ContentType.objects.get_for_model(Challenge):
            challenge = get_object_or_404(Challenge, pk=object_id)
            slides.append({"challenge": challenge})

    return slides


def get_question_index(user: User, position: int) -> int:
    questions = LevelSequence.objects.filter(
        level=user.current_level,
        content_type=ContentType.objects.get_for_model(Question),
    ).order_by("position")
    index = questions.filter(position__lte=position).count()
    return index


def set_status_carousel_controls(user: User) -> [bool, bool]:
    try:
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

        previous_control_enable = bool(sequence_before)
        next_control_enable = bool(sequence_after)

    except LevelSequence.DoesNotExist:
        previous_control_enable = False
        next_control_enable = False

    return [previous_control_enable, next_control_enable]
