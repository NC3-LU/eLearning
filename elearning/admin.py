from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from parler.admin import TranslatableAdmin

from .models import (
    Category,
    Challenge,
    Context,
    ContextMediaTemplate,
    Level,
    Media,
    Option,
    Question,
    QuestionMediaTemplate,
    Resource,
)


class LevelsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    complexity = fields.Field(column_name="complexity", attribute="complexity")
    duration = fields.Field(column_name="duration", attribute="duration")
    plot = fields.Field(column_name="plot", attribute="plot")
    objectives = fields.Field(column_name="objectives", attribute="objectives")
    requirements = fields.Field(column_name="requirements", attribute="requirements")

    class Meta:
        model = Level


@admin.register(Level)
class LevelAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "complexity", "duration")
    fields = ("name", "complexity", "duration", "plot", "objectives", "requirements")
    resource_class = LevelsResource


class CategoriesResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=ForeignKeyWidget(Level, field="name"),
    )

    class Meta:
        model = Category


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "level", "index")
    list_filter = ("level",)
    fields = ["index", "name", "level"]
    resource_class = CategoriesResource


class OptionsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    is_correct = fields.Field(column_name="is_correct", attribute="is_correct")
    score = fields.Field(column_name="score", attribute="score")
    tooltip = fields.Field(column_name="tooltip", attribute="tooltip")

    class Meta:
        model = Option


@admin.register(Option)
class OptionAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "index", "score", "is_correct")
    list_filter = ("is_correct",)
    fields = ("index", "name", "is_correct", "score", "tooltip")
    resource_class = OptionsResource


class MediasResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    path = fields.Field(column_name="path", attribute="path")
    m_type = fields.Field(column_name="type", attribute="m_type")

    class Meta:
        model = Media


@admin.register(Media)
class MediaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("name", "path", "m_type")
    search_fields = ("name", "m_type")
    fields = ("name", "path", "m_type")
    resource_class = MediasResource


class QuestionsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    q_type = fields.Field(column_name="type", attribute="q_type")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=ForeignKeyWidget(Level, field="name"),
    )
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )
    max_score = fields.Field(column_name="max_score", attribute="max_score")

    path = fields.Field(column_name="path", attribute="path")
    m_type = fields.Field(column_name="type", attribute="m_type")
    explanation = fields.Field(column_name="explanation", attribute="explanation")
    tooltip = fields.Field(column_name="tooltip", attribute="tooltip")
    options = fields.Field(
        column_name="options",
        attribute="options",
        widget=ManyToManyWidget(Option, field="name", separator=","),
    )
    medias = fields.Field(
        column_name="medias",
        attribute="medias",
        widget=ManyToManyWidget(Media, field="name", separator=","),
    )

    class Meta:
        model = Question


class questionOptionsInline(admin.TabularInline):
    model = Question.options.through
    verbose_name = "Option"
    verbose_name_plural = "Options"
    extra = 0


class questionMediaInline(admin.TabularInline):
    model = QuestionMediaTemplate
    verbose_name = "Media"
    verbose_name_plural = "Medias"
    extra = 0


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = (
        "name",
        "index",
        "q_type",
        "level",
        "category",
        "max_score",
    )
    list_filter = ("level", "category", "q_type")
    fields = (
        "index",
        "name",
        "q_type",
        "level",
        "category",
        "max_score",
        "explanation",
        "tooltip",
    )
    inlines = (questionOptionsInline, questionMediaInline)
    resource_class = QuestionsResource


class ContextsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    question = fields.Field(
        column_name="question",
        attribute="question",
        widget=ForeignKeyWidget(Question, field="name"),
    )
    medias = fields.Field(
        column_name="medias",
        attribute="medias",
        widget=ManyToManyWidget(Media, field="name", separator=","),
    )

    class Meta:
        model = Context


class contextMediaInline(admin.TabularInline):
    model = ContextMediaTemplate
    verbose_name = "Media"
    verbose_name_plural = "Medias"
    extra = 0


@admin.register(Context)
class ContextAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("index", "question", "name")
    list_filter = ("question",)
    fields = ("index", "question", "name")
    inlines = (contextMediaInline,)
    resource_class = ContextsResource


class ResourcesResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=ForeignKeyWidget(Level, field="name"),
    )

    class Meta:
        model = Resource


@admin.register(Resource)
class ResourceAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "level")
    list_filter = ("level",)


class ChallengesResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=ForeignKeyWidget(Level, field="name"),
    )

    class Meta:
        model = Challenge


@admin.register(Challenge)
class ChallengeAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "level")
    list_filter = ("level",)
