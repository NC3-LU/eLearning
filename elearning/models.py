import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from .globals import MEDIA_TYPE, POSITION_CHOICES, QUESTION_TYPES, TEXT_TYPE


# Levels
class Level(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="label"),
        description=models.TextField(),
    )

    def get_first_level_position(self) -> int:
        first_level_sequence = self.levelsequence_set.order_by("position").first()
        if first_level_sequence:
            return first_level_sequence.position
        return None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")


# Categories
class Category(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(name=models.CharField(max_length=100))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


# Answer choices
class AnswerChoice(TranslatableModel):
    translations = TranslatedFields(
        name=models.TextField(verbose_name="label"),
        tooltip=models.TextField(blank=True, default=None, null=True),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Answer choice")
        verbose_name_plural = _("Answer choices")


# Medias
class Media(models.Model):
    name = models.CharField(max_length=100, verbose_name="label")
    path = models.FilePathField(path=settings.MEDIA_DIR, recursive=True)
    m_type = models.CharField(
        max_length=1, choices=MEDIA_TYPE, default=MEDIA_TYPE[0][0], verbose_name="type"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Medias")


class Text(TranslatableModel):
    name = models.CharField(max_length=100, verbose_name="label")
    translations = TranslatedFields(
        description=models.TextField(blank=True, default=None, null=True),
        hyperlink=models.TextField(blank=True, default=None, null=True),
    )
    t_type = models.CharField(
        max_length=1, choices=TEXT_TYPE, default=TEXT_TYPE[0][0], verbose_name="type"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Text")
        verbose_name_plural = _("Texts")


# Questions
class Question(TranslatableModel):
    translations = TranslatedFields(
        name=models.TextField(verbose_name="label"),
        tooltip=models.TextField(blank=True, default=None, null=True),
    )
    q_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=QUESTION_TYPES[0][0],
        verbose_name="type",
    )
    categories = models.ManyToManyField(Category, blank=True, default=None)
    answer_choices = models.ManyToManyField(
        AnswerChoice, through="QuestionAnswerChoice"
    )
    medias = models.ManyToManyField(Media, through="QuestionMediaTemplate")
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


# Question explanation
class Explanation(TranslatableModel):
    translations = TranslatedFields(name=models.TextField(verbose_name="Label"))
    medias = models.ManyToManyField(Media, through="ExplanationMediaTemplate")
    texts = models.ManyToManyField(Text, through="ExplanationTextTemplate")
    question = models.ForeignKey(
        Question, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Explanation")
        verbose_name_plural = _("Explanations")


# Quizzes
class Quiz(TranslatableModel):
    translations = TranslatedFields(
        name=models.TextField(verbose_name="label"),
        tooltip=models.TextField(blank=True, default=None, null=True),
    )
    questions = models.ManyToManyField(Question, through="QuizQuestion")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")


# Contexts
class Context(TranslatableModel):
    translations = TranslatedFields(name=models.TextField(verbose_name="Title"))
    medias = models.ManyToManyField(Media, through="ContextMediaTemplate")
    texts = models.ManyToManyField(Text, through="ContextTextTemplate")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Context")
        verbose_name_plural = _("Contexts")


# Users
class User(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    current_level = models.ForeignKey(Level, null=True, on_delete=models.CASCADE)
    current_position = models.PositiveSmallIntegerField(null=True)
    created_at = models.DateField(auto_now_add=True, blank=True)
    updated_at = models.DateField(auto_now=True, blank=True)

    def get_level_progress(self) -> int:
        return (
            self.score_set.filter(level=self.current_level)
            .values_list("progress", flat=True)
            .first()
        )

    class Meta:
        verbose_name = _("Users")
        verbose_name_plural = _("Users")


# Answers
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_choices = models.ManyToManyField(AnswerChoice)

    def __str__(self):
        return str(self.answer_choices)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


# Resources Types
class ResourceType(TranslatableModel):
    index = models.PositiveIntegerField()
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Resource Type")
        verbose_name_plural = _("Resource Types")


# Resources
class Resource(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        description=models.TextField(blank=True, default=None, null=True),
    )
    level = models.ForeignKey(
        Level,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    resourceType = models.ForeignKey(
        ResourceType, models.SET_NULL, blank=True, null=True, verbose_name="type"
    )

    path = models.FilePathField(path=settings.MEDIA_DIR, recursive=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")


# Challenges
class Challenge(TranslatableModel):
    translations = TranslatedFields(
        name=models.TextField(),
        description=models.TextField(blank=True, default=None, null=True),
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Challenge")
        verbose_name_plural = _("Challenges")


# Scores
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    score = models.DecimalField(
        default=0, max_digits=5, decimal_places=2, validators=[MaxValueValidator(100)]
    )
    progress = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return str(self.score)

    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")


# Knowledges
class Knowledge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    progress = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.progress)

    class Meta:
        verbose_name = _("Knowledge")
        verbose_name_plural = _("Knowledge")


# Level Sequence
class LevelSequence(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        unique_together = ("level", "position")


class ContextMediaTemplate(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )
    css_classes = ArrayField(models.CharField(), default=list, blank=True)

    class Meta:
        verbose_name = _("Media Template")
        verbose_name_plural = _("Media Templates")

    def __str__(self):
        return ""


class ContextTextTemplate(models.Model):
    index = models.PositiveSmallIntegerField()
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )
    css_classes = ArrayField(models.CharField(), default=list, blank=True)

    class Meta:
        verbose_name = _("Text Template")
        verbose_name_plural = _("Text Templates")

    def __str__(self):
        return ""


class QuestionMediaTemplate(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )
    css_classes = ArrayField(models.CharField(), default=list, blank=True)

    class Meta:
        verbose_name = _("Media Template")
        verbose_name_plural = _("Media Templates")

    def __str__(self):
        return ""


class ExplanationMediaTemplate(models.Model):
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )
    css_classes = ArrayField(models.CharField(), default=list, blank=True)

    class Meta:
        verbose_name = _("Media Template")
        verbose_name_plural = _("Media Templates")

    def __str__(self):
        return ""


class ExplanationTextTemplate(models.Model):
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )
    css_classes = ArrayField(models.CharField(), default=list, blank=True)

    class Meta:
        verbose_name = _("Text Template")
        verbose_name_plural = _("Text Templates")

    def __str__(self):
        return ""


class QuestionAnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(default=0)
    is_correct = models.BooleanField(
        verbose_name="Is it the correct answer ?", default=False
    )
    score = models.IntegerField(default=0)
    answerChoice = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Question Answer Choice")
        verbose_name_plural = _("Question Answer Choices")

    def __str__(self):
        return ""


class QuizQuestion(models.Model):
    index = models.PositiveSmallIntegerField()
    display_quiz_label = models.BooleanField(
        verbose_name="Display label quiz?", default=True
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Quiz Question")
        verbose_name_plural = _("Quiz Questions")

    def __str__(self):
        return ""
