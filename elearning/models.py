import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from .globals import POSITION_CHOICES, QUESTION_TYPES, STATUS_LEVEL


# Levels
class Level(TranslatableModel):
    translations = TranslatedFields(name=models.TextField())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")


# Categories
class Category(TranslatableModel):
    translations = TranslatedFields(name=models.TextField())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


# Options
class Option(TranslatableModel):
    index = models.IntegerField(unique=True)
    translations = TranslatedFields(
        name=models.TextField(),
        tooltip=models.TextField(null=False, blank=True, default=""),
    )
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Option")
        verbose_name_plural = _("Options")


# Medias
class Media(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    position = models.CharField(
        max_length=2, choices=POSITION_CHOICES, default=POSITION_CHOICES[0][0]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Medias")


# Contexts
class Context(TranslatableModel):
    translations = TranslatedFields(name=models.TextField())
    media = models.ManyToManyField(Media)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Context")
        verbose_name_plural = _("Contexts")


# Questions
class Question(TranslatableModel):
    index = models.IntegerField(unique=True)
    translations = TranslatedFields(
        name=models.TextField(),
        tooltip=models.TextField(null=False, blank=True, default=""),
    )
    q_type = models.CharField(
        max_length=2, choices=QUESTION_TYPES, default=QUESTION_TYPES[0][0]
    )
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    options = models.ManyToManyField(Option)
    media = models.ManyToManyField(Media)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


# Learners
class learner(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    current_level = models.ForeignKey(Level, on_delete=models.CASCADE)
    current_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    status_level = models.CharField(
        max_length=1, choices=STATUS_LEVEL, default=STATUS_LEVEL[0][0]
    )
    created_at = models.DateField(auto_now_add=True, blank=True)
    updated_at = models.DateField(auto_now=True, blank=True)

    class Meta:
        verbose_name = _("Learner")
        verbose_name_plural = _("Learners")


# Answers
class answer(models.Model):
    learner = models.ForeignKey(learner, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ManyToManyField(Option)

    def __str__(self):
        return str(self.option)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
