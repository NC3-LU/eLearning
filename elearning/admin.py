from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget, Widget
from parler.admin import TranslatableAdmin
from parler.models import TranslationDoesNotExist

from .globals import COMPLEXITY_LEVEL, MEDIA_TYPE, QUESTION_TYPES, TEXT_TYPE
from .models import (
    AnswerChoice,
    Category,
    Challenge,
    Context,
    ContextMediaTemplate,
    ContextTextTemplate,
    Level,
    Media,
    Question,
    QuestionMediaTemplate,
    Resource,
    Text,
)
from .settings import LANGUAGES, SITE_NAME


class CustomAdminSite(admin.AdminSite):
    site_header = SITE_NAME + " " + "Administration"
    site_title = SITE_NAME


admin_site = CustomAdminSite()


# Widget that uses choice display values in place of database values
class ChoicesWidget(Widget):
    def __init__(self, choices, *args, **kwargs):
        self.choices = dict(choices)
        self.revert_choices = {v: k for k, v in self.choices.items()}

    def clean(self, value, row=None, *args, **kwargs):
        return self.revert_choices.get(value, value) if value else None

    def render(self, value, obj=None):
        return self.choices.get(value, "")


# Custom widget to handle translated M2M relationships
class TranslatedNameM2MWidget(widgets.ManyToManyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()

        names = value.split(self.separator)
        languages = [lang[0] for lang in LANGUAGES]

        instances = []
        for name in names:
            for lang_code in languages:
                try:
                    instance = self.model._parler_meta.root_model.objects.get(
                        name=name.strip(),
                        language_code=lang_code,
                    )
                    instances.append(instance.master_id)
                    break
                except (self.model.DoesNotExist, TranslationDoesNotExist):
                    pass

        return instances


# Custom widget to handle translated ForeignKey relationships
class TranslatedNameWidget(widgets.ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()

        languages = [lang[0] for lang in LANGUAGES]

        for lang_code in languages:
            try:
                instance = self.model._parler_meta.root_model.objects.get(
                    name=value.strip(),
                    language_code=lang_code,
                )
                return instance.master
            except (self.model.DoesNotExist, TranslationDoesNotExist):
                pass

        return


class LevelsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    complexity = fields.Field(
        column_name="complexity",
        attribute="complexity",
        widget=ChoicesWidget(COMPLEXITY_LEVEL),
    )
    duration = fields.Field(column_name="duration", attribute="duration")
    plot = fields.Field(column_name="plot", attribute="plot")
    objectives = fields.Field(column_name="objectives", attribute="objectives")
    requirements = fields.Field(column_name="requirements", attribute="requirements")

    class Meta:
        model = Level


@admin.register(Level, site=admin_site)
class LevelAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("index", "name", "complexity", "duration")
    list_display_links = ["index", "name"]
    fields = (
        "index",
        "name",
        "complexity",
        "duration",
        "plot",
        "objectives",
        "requirements",
    )
    resource_class = LevelsResource
    ordering = ["index"]


class CategoriesResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=TranslatedNameWidget(Level, field="name"),
    )

    class Meta:
        model = Category


@admin.register(Category, site=admin_site)
class CategoryAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = (
        "index",
        "name",
        "level",
    )
    list_filter = ("level",)
    fields = ["index", "name", "level"]
    list_display_links = ["index", "name"]
    resource_class = CategoriesResource
    ordering = ["level__index", "index"]


class AnswerChoicesResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    is_correct = fields.Field(column_name="is_correct", attribute="is_correct")
    score = fields.Field(column_name="score", attribute="score")
    tooltip = fields.Field(column_name="tooltip", attribute="tooltip")

    class Meta:
        model = AnswerChoice


@admin.register(AnswerChoice, site=admin_site)
class AnswerChoiceAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "index", "score", "is_correct")
    list_filter = ("is_correct",)
    fields = ("index", "name", "is_correct", "score", "tooltip")
    resource_class = AnswerChoicesResource


class MediasResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    path = fields.Field(column_name="path", attribute="path")
    m_type = fields.Field(
        column_name="type", attribute="m_type", widget=ChoicesWidget(MEDIA_TYPE)
    )

    class Meta:
        model = Media


@admin.register(Media, site=admin_site)
class MediaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("name", "path", "m_type")
    search_fields = ("name", "m_type")
    fields = ("name", "path", "m_type")
    resource_class = MediasResource


class TextsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    t_type = fields.Field(
        column_name="type", attribute="m_type", widget=ChoicesWidget(TEXT_TYPE)
    )
    description = fields.Field(column_name="description", attribute="description")
    hyperlink = fields.Field(column_name="hyperlink", attribute="hyperlink")

    class Meta:
        model = Text


@admin.register(Text, site=admin_site)
class TextAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "t_type")
    search_fields = ("name", "t_type")
    fields = ("name", "t_type", "description", "hyperlink")
    resource_class = TextsResource


class QuestionsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="label", attribute="name")
    q_type = fields.Field(
        column_name="type", attribute="q_type", widget=ChoicesWidget(QUESTION_TYPES)
    )
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=TranslatedNameWidget(Level, field="name"),
    )
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=TranslatedNameWidget(Category, field="name"),
    )
    max_score = fields.Field(column_name="max_score", attribute="max_score")
    explanation = fields.Field(column_name="explanation", attribute="explanation")
    tooltip = fields.Field(column_name="tooltip", attribute="tooltip")
    answer_choices = fields.Field(
        column_name="answer choices",
        attribute="answer_choices",
        widget=TranslatedNameM2MWidget(AnswerChoice, field="name", separator="\n"),
    )
    medias = fields.Field(
        column_name="medias",
        attribute="medias",
        widget=ManyToManyWidget(Media, field="name", separator=","),
    )

    class Meta:
        model = Question


class questionAnswerChoicesInline(admin.TabularInline):
    model = Question.answer_choices.through
    verbose_name = "Answer choice"
    verbose_name_plural = "Answer choices"
    extra = 0


class questionMediaInline(admin.TabularInline):
    model = QuestionMediaTemplate
    verbose_name = "Media"
    verbose_name_plural = "Medias"
    extra = 0


@admin.register(Question, site=admin_site)
class QuestionAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = (
        "index",
        "name",
        "q_type",
        "level",
        "category",
        "max_score",
    )
    list_filter = ("level", "category", "q_type")
    list_display_links = ["index", "name"]
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
    inlines = (
        questionAnswerChoicesInline,
        questionMediaInline,
    )
    resource_class = QuestionsResource

    ordering = ["level__index", "category__index", "index"]


class ContextsResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    question = fields.Field(
        column_name="question",
        attribute="question",
        widget=TranslatedNameWidget(Question, field="name"),
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


class contextTextInline(admin.TabularInline):
    model = ContextTextTemplate
    verbose_name = "Text"
    verbose_name_plural = "Texts"
    extra = 0


@admin.register(Context, site=admin_site)
class ContextAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("index", "question", "name")
    list_filter = ("question",)
    fields = ("index", "question", "name")
    inlines = (contextMediaInline, contextTextInline)
    resource_class = ContextsResource


class ResourcesResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    description = fields.Field(column_name="description", attribute="description")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=TranslatedNameWidget(Level, field="name"),
    )
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=TranslatedNameWidget(Category, field="name"),
    )

    class Meta:
        model = Resource


@admin.register(Resource, site=admin_site)
class ResourceAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "level", "description")
    list_filter = ("level", "category")


class ChallengesResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=TranslatedNameWidget(Level, field="name"),
    )

    class Meta:
        model = Challenge


@admin.register(Challenge, site=admin_site)
class ChallengeAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "level")
    list_filter = ("level",)
