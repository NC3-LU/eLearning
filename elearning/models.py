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
)


# Levels
class Level(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
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
    translations = TranslatedFields(name=models.CharField(max_length=100))
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


# Options
class Option(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(
        name=models.TextField(),
        tooltip=models.TextField(null=False, blank=True, default=""),
    )
    score = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Option")
        verbose_name_plural = _("Options")


# Medias
class Media(models.Model):
    name = models.CharField(max_length=100)
    path = models.FilePathField(path=settings.MEDIA_DIR, recursive=True)
    m_type = models.CharField(
        max_length=1, choices=MEDIA_TYPE, default=MEDIA_TYPE[0][0], verbose_name="type"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Medias")


# Questions
class Question(TranslatableModel):
    index = models.IntegerField(unique=True)
    translations = TranslatedFields(
        name=models.TextField(),
        explanation=models.TextField(),
        tooltip=models.TextField(null=False, blank=True, default=""),
    )
    q_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=QUESTION_TYPES[0][0],
        verbose_name="type",
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    options = models.ManyToManyField(Option)
    media = models.ManyToManyField(Media, through="QuestionMediaTemplate")
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


# Contexts
class Context(TranslatableModel):
    index = models.IntegerField()
    translations = TranslatedFields(name=models.TextField())
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    medias = models.ManyToManyField(Media, through="ContextMediaTemplate")

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
    option = models.ManyToManyField(Option)

    def __str__(self):
        return str(self.option)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


# Resources
class Resource(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.option)

    class Meta:
        verbose_name = _("Ressource")
        verbose_name_plural = _("Ressources")


# Challenges
class Challenge(TranslatableModel):
    translations = TranslatedFields(
        name=models.TextField(),
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
