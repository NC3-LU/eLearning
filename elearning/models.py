import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from .globals import (
    COMPLEXITY_LEVEL,
    MEDIA_TYPE,
    POSITION_CHOICES,
    QUESTION_TYPES,
    STATUS_LEVEL,
    TEXT_TYPE,
)


# Levels
class Level(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="label"),
        plot=models.TextField(),
        objectives=models.TextField(),
        requirements=models.TextField(),
    )
    duration = models.IntegerField()
    complexity = models.CharField(
        max_length=1, choices=COMPLEXITY_LEVEL, default=COMPLEXITY_LEVEL[0][0]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")


# Categories
class Category(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="label")
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


# Answer choices
class AnswerChoice(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(
        name=models.TextField(verbose_name="label"),
        tooltip=models.TextField(blank=True, default=None, null=True),
    )
    score = models.IntegerField(default=0)
    is_correct = models.BooleanField(
        verbose_name="Is it the correct answer ?", default=False
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
    )
    t_type = models.CharField(
        max_length=1, choices=TEXT_TYPE, default=TEXT_TYPE[0][0], verbose_name="type"
    )
    hyperlink = models.TextField(blank=True, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Text")
        verbose_name_plural = _("Texts")


# Questions
class Question(TranslatableModel):
    index = models.IntegerField(unique=True)
    translations = TranslatedFields(
        name=models.TextField(verbose_name="label"),
        explanation=models.TextField(),
        tooltip=models.TextField(blank=True, default=None, null=True),
    )
    q_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=QUESTION_TYPES[0][0],
        verbose_name="type",
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    answer_choices = models.ManyToManyField(AnswerChoice)
    medias = models.ManyToManyField(Media, through="QuestionMediaTemplate")
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


# Contexts
class Context(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(name=models.TextField(verbose_name="Title"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
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
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    status_level = models.CharField(
        max_length=1, choices=STATUS_LEVEL, default=STATUS_LEVEL[0][0]
    )
    created_at = models.DateField(auto_now_add=True, blank=True)
    updated_at = models.DateField(auto_now=True, blank=True)

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


# Resources
class Resource(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100, verbose_name="label"),
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Ressource")
        verbose_name_plural = _("Ressources")


# Challenges
class Challenge(TranslatableModel):
    translations = TranslatedFields(
        name=models.TextField(verbose_name="description"),
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Challenge")
        verbose_name_plural = _("Challenges")


class ContextMediaTemplate(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )
    css_classes = ArrayField(models.CharField(max_length=50, blank=True), default=list)

    class Meta:
        verbose_name = _("Media Template")
        verbose_name_plural = _("Media Templates")

    def __str__(self):
        return ""


class ContextTextTemplate(models.Model):
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )
    css_classes = ArrayField(models.CharField(max_length=50, blank=True), default=list)

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
    css_classes = ArrayField(models.CharField(max_length=50, blank=True), default=list)

    class Meta:
        verbose_name = _("Media Template")
        verbose_name_plural = _("Media Templates")

    def __str__(self):
        return ""
