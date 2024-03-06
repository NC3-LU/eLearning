import os
from collections import Counter, OrderedDict
from typing import List
from uuid import UUID

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, F, OuterRef, Q, QuerySet, Subquery
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from weasyprint import CSS, HTML

from .forms import AnswerForm
from .models import (
    AnswerChoice,
    Context,
    ContextResourceTemplate,
    Explanation,
    Knowledge,
    Level,
    LevelSequence,
    Question,
    QuestionAnswerChoice,
    QuizQuestion,
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


def set_progress_course(user: User, quizzes: OrderedDict):
    level_sequence = LevelSequence.objects.filter(level=user.current_level).order_by(
        "position"
    )
    user_score = user.score_set.filter(level=user.current_level).first()

    if not level_sequence or not user_score:
        return

    nb_quizzes = len(quizzes)
    nb_questions_quiz = sum(value["nb_questions"] for value in quizzes.values())

    total_positions = level_sequence.count() - nb_questions_quiz + nb_quizzes

    if total_positions <= 0:
        return

    total_nb_questions_before, count_before = items_before_position(
        quizzes, user.current_position
    )

    index = (
        level_sequence.filter(position__lte=user.current_position).count()
        - total_nb_questions_before
        + count_before
    )

    progress = (index / total_positions) * 100

    current_level_sequence = level_sequence.get(position=user.current_position)
    question_content_type = ContentType.objects.get_for_model(Question)

    if (
        current_level_sequence.content_type == question_content_type
        and current_level_sequence.content_object.quiz_set.exists()
    ):
        quiz = current_level_sequence.content_object.quiz_set.first()
        progress = quizzes[quiz.id]["percentage"]

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

    total_correct_choices = QuestionAnswerChoice.objects.filter(
        question__id__in=object_ids_all, is_correct=True
    ).count()

    if question.q_type == "SR":
        user_answers_are_correct = sum(
            x == str(y)
            for x, y in zip(
                user_answer_choices,
                question.answer_choices.order_by(
                    "questionanswerchoice__index"
                ).values_list("id", flat=True),
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


def get_slides_content(user: User, direction: str) -> List:
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
                        "label": context.name,
                        "texts": context.contexttexttemplate_set.all().order_by(
                            "index"
                        ),
                        "medias": context.contextmediatemplate_set.all(),
                        "resources": context.contextresourcetemplate_set.all().order_by(
                            "index"
                        ),
                    }
                }
            )
        elif content_type == ContentType.objects.get_for_model(Question):
            question = get_object_or_404(Question, pk=object_id)
            form = AnswerForm(question=question, user=user)
            form.quiz_index = (
                get_quiz_index(user, sequence.content_object.quiz_set.first().id)
                if form.quiz
                else None
            )
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

    return slides


def get_questions_level_sequences(
    user: User, is_quiz: bool = False
) -> QuerySet[LevelSequence]:
    question_content_type = ContentType.objects.get_for_model(Question)
    level_sequences = (
        LevelSequence.objects.filter(
            level=user.current_level, content_type=question_content_type
        )
        .annotate(
            is_related_to_quiz=Exists(
                QuizQuestion.objects.filter(question_id=OuterRef("object_id"))
            )
        )
        .filter(is_related_to_quiz=is_quiz)
        .order_by("position")
    )

    return level_sequences


def get_question_index(user: User, position: int) -> int:
    questions = get_questions_level_sequences(user)
    index = questions.filter(position__lte=position).count()
    return index


def get_quiz_index(user: User, quiz_id: int) -> int:
    quiz_order = get_quiz_order(user)
    index = quiz_order[quiz_id]["index"]
    return index


def get_quiz_order(user: User) -> OrderedDict:
    quiz_ordered = OrderedDict()
    all_level_sequence = LevelSequence.objects.filter(
        level=user.current_level
    ).order_by("position")
    questions_quiz_level_sequences = get_questions_level_sequences(user, is_quiz=True)
    index = 1
    total_questions = 0
    for sequence in questions_quiz_level_sequences:
        quiz = sequence.content_object.quiz_set.first()
        nb_questions = quiz.quizquestion_set.count()
        position = all_level_sequence.filter(position__lte=sequence.position).count()
        if quiz.id not in quiz_ordered:
            quiz_ordered[quiz.id] = {
                "index": index,
                "position": position,
                "nb_questions": nb_questions,
            }
            total_questions += nb_questions
            index += 1

    total_slides = all_level_sequence.count() - total_questions + len(quiz_ordered)

    for _quiz_id, quiz in quiz_ordered.items():
        total_nb_questions_before, count_before = items_before_position(
            quiz_ordered, quiz["position"]
        )

        quiz["percentage"] = (
            (quiz["position"] - total_nb_questions_before + count_before) / total_slides
        ) * 100

    return quiz_ordered


def items_before_position(ordered_dict: OrderedDict, current_position: int) -> tuple:
    total_nb_questions = 0
    count = 0
    for _key, value in ordered_dict.items():
        if value["position"] < current_position:
            total_nb_questions += value["nb_questions"]
            count += 1
    return total_nb_questions, count


def set_status_carousel_controls(user: User) -> List[bool]:
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


def get_allowed_resources_ids(user: User) -> List:
    context_content_type = ContentType.objects.get_for_model(Context)
    contextResource_subquery = ContextResourceTemplate.objects.filter(
        context_id=OuterRef("object_id")
    ).values("context_id")

    context_sequences = LevelSequence.objects.filter(
        content_type=context_content_type,
        level__lte=user.current_level,
        object_id__in=Subquery(contextResource_subquery),
    )

    allowed_resources_set = set()

    if not user.current_level:
        return list(allowed_resources_set)

    for sequence in context_sequences:
        if (
            sequence.level == user.current_level
            and user.current_position
            and sequence.position <= user.current_position
        ):
            allowed_resources_set.update(
                sequence.content_object.resources.values_list("id", flat=True)
            )
        elif sequence.level.index < user.current_level.index:
            allowed_resources_set.update(
                sequence.content_object.resources.values_list("id", flat=True)
            )

    return list(allowed_resources_set)


def get_questions_and_quizzes(user: User) -> List:
    questions_and_quizzes = []
    question_content_type = ContentType.objects.get_for_model(Question)
    level_sequence = LevelSequence.objects.filter(
        level=user.current_level, content_type=question_content_type
    ).order_by("position")
    for sequence in level_sequence:
        question = get_object_or_404(Question, pk=sequence.object_id)
        form = AnswerForm(question=question, user=user)
        form.quiz_index = (
            get_quiz_index(user, sequence.content_object.quiz_set.first().id)
            if form.quiz
            else None
        )
        form.question_index = get_question_index(user, sequence.position)
        questions_and_quizzes.append(form)

    return questions_and_quizzes


def get_report_pdf(user: User, request: HttpRequest) -> bytes:
    html_string = render_to_string(
        "report/template.html",
        {
            "index_level": user.current_level.index,
            "name_level": user.current_level.name,
            "score_level": Score.objects.get(user=user, level=user.current_level).score,
            "static_theme_dir": os.path.abspath(settings.STATIC_THEME_DIR),
            "user_id": user.uuid,
            "end_level_date": user.updated_at,
            "questions_and_quizzes": get_questions_and_quizzes(user),
        },
        request=request,
    )

    htmldoc = HTML(string=html_string)
    stylesheets = [
        CSS(os.path.join(settings.STATIC_THEME_DIR, "css/custom.css")),
        CSS(os.path.join(settings.STATIC_THEME_DIR, "css/report.css")),
    ]

    return htmldoc.write_pdf(stylesheets=stylesheets)
