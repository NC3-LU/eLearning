from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.db.models import OuterRef, Subquery
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
from parler.admin import TranslatableAdmin

from .globals import MEDIA_TYPE, QUESTION_TYPES, TEXT_TYPE
from .mixins import TranslationImportMixin
from .models import (
    AnswerChoice,
    AnswerChoiceCategory,
    Category,
    Challenge,
    Context,
    ContextMediaTemplate,
    ContextTextTemplate,
    Level,
    LevelSequence,
    Media,
    Question,
    QuestionMediaTemplate,
    Resource,
    ResourceType,
    Text,
)
from .settings import SITE_NAME
from .widgets import ChoicesWidget, TranslatedNameM2MWidget, TranslatedNameWidget


class CustomAdminSite(admin.AdminSite):
    site_header = SITE_NAME + " " + "Administration"
    site_title = SITE_NAME


admin_site = CustomAdminSite()


class LevelsResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    description = fields.Field(column_name="description", attribute="description")

    class Meta:
        model = Level


# Generic Relation Level Sequence Inline Field
class levelSequenceInline(GenericTabularInline):
    model = LevelSequence
    extra = 0
    max_num = 1


@admin.register(Level, site=admin_site)
class LevelAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("index", "name", "description")
    list_display_links = ["index", "name"]
    fields = (
        "index",
        "name",
        "description",
    )
    resource_class = LevelsResource
    ordering = ["index"]


class CategoriesResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")

    class Meta:
        model = Category


@admin.register(Category, site=admin_site)
class CategoryAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = (
        "index",
        "name",
    )
    fields = ["index", "name"]
    list_display_links = ["index", "name"]
    resource_class = CategoriesResource
    ordering = ["index"]


class AnswerChoicesResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    index = fields.Field(column_name="index", attribute="index")
    name = fields.Field(column_name="name", attribute="name")
    is_correct = fields.Field(column_name="is_correct", attribute="is_correct")
    score = fields.Field(column_name="score", attribute="score")
    tooltip = fields.Field(column_name="tooltip", attribute="tooltip")
    answer_text = fields.Field(column_name="answer_text", attribute="answer_text")
    answer_choice_category = fields.Field(
        column_name="answer_choice_category",
        attribute="answer_choice_category",
        saves_null_values=False,
        default=None,
        widget=TranslatedNameWidget(AnswerChoiceCategory, field="name"),
    )

    class Meta:
        model = AnswerChoice


@admin.register(AnswerChoice, site=admin_site)
class AnswerChoiceAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = (
        "name",
        "index",
        "score",
        "is_correct",
        "answer_text",
        "answer_choice_category",
    )
    list_filter = ("is_correct",)
    fields = (
        "index",
        "name",
        "is_correct",
        "score",
        "tooltip",
        "answer_text",
        "answer_choice_category",
    )
    resource_class = AnswerChoicesResource


class AnswerChoiceCategoriesResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")

    class Meta:
        model = AnswerChoiceCategory


@admin.register(AnswerChoiceCategory, site=admin_site)
class AnswerChoiceCategoriesAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name",)
    fields = ("name",)
    resource_class = AnswerChoiceCategoriesResource


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


class TextsResource(TranslationImportMixin, resources.ModelResource):
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


class QuestionsResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="label", attribute="name")
    q_type = fields.Field(
        column_name="type", attribute="q_type", widget=ChoicesWidget(QUESTION_TYPES)
    )
    categories = fields.Field(
        column_name="categories",
        attribute="categories",
        widget=TranslatedNameM2MWidget(Category, field="name", separator="\n"),
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
        "name",
        "q_type",
        "max_score",
        "level_sequence_level",
        "level_sequence_position",
        "display_categories",
    )
    list_filter = ("q_type",)
    list_display_links = ["name"]
    fields = (
        "name",
        "q_type",
        "max_score",
        "explanation",
        "tooltip",
        "categories",
    )
    filter_horizontal = ["categories"]
    inlines = (
        questionAnswerChoicesInline,
        questionMediaInline,
        levelSequenceInline,
    )
    resource_class = QuestionsResource

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        levelSequences = LevelSequence.objects.filter(
            content_type=ContentType.objects.get_for_model(Question),
            object_id=OuterRef("id"),
        ).order_by()
        level_sequence_levels = levelSequences.values("level")[:1]
        level_sequence_positions = levelSequences.values("position")[:1]
        return queryset.annotate(
            level_sequence_level=Subquery(level_sequence_levels),
            level_sequence_position=Subquery(level_sequence_positions),
        )

    @admin.display(description="Categories")
    def display_categories(self, obj):
        return "\n".join([category.name for category in obj.categories.all()])

    @admin.display(description="Level", ordering="level_sequence_level")
    def level_sequence_level(self, obj):
        level_sequence = LevelSequence.objects.filter(object_id=obj.id).first()
        if level_sequence:
            return level_sequence.level
        return None

    @admin.display(description="Position", ordering="level_sequence_position")
    def level_sequence_position(self, obj):
        level_sequence = LevelSequence.objects.filter(object_id=obj.id).first()
        if level_sequence:
            return level_sequence.position
        return None


class ContextsResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
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
    list_display = ("name",)
    fields = ("name",)
    inlines = (contextMediaInline, contextTextInline, levelSequenceInline)
    resource_class = ContextsResource


class ResourcesResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    description = fields.Field(column_name="description", attribute="description")
    level = fields.Field(
        column_name="level",
        attribute="level",
        widget=TranslatedNameWidget(Level, field="name"),
    )
    resourceType = fields.Field(
        column_name="resourceType",
        attribute="resourceType",
        widget=TranslatedNameWidget(ResourceType, field="name"),
    )

    class Meta:
        model = Resource


@admin.register(Resource, site=admin_site)
class ResourceAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("name", "level", "resourceType", "description")
    list_filter = ("level", "resourceType")
    resource_class = ResourcesResource
    ordering = ["level__index"]


class ResourcesResourceType(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")

    class Meta:
        model = ResourceType


@admin.register(ResourceType, site=admin_site)
class ResourceTypeAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ("index", "name")
    list_display_links = ["index", "name"]
    ordering = ["index"]
    resource_class = ResourcesResourceType


class ChallengesResource(TranslationImportMixin, resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id", readonly=True)
    name = fields.Field(column_name="name", attribute="name")
    description = fields.Field(column_name="description", attribute="description")

    class Meta:
        model = Challenge


@admin.register(Challenge, site=admin_site)
class ChallengeAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = (
        "name",
        "description",
    )
    inlines = (levelSequenceInline,)


@admin.register(LevelSequence, site=admin_site)
class LevelSequenceAdmin(admin.ModelAdmin):
    list_display = ("level", "position", "get_content_type_name", "content_object_str")
    list_filter = ("level",)
    ordering = ["level__index", "position"]

    @admin.display(description="Content Type")
    def get_content_type_name(self, obj):
        return obj.content_type.model

    @admin.display(description="Content")
    def content_object_str(self, obj):
        return str(obj.content_object)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            allowed_models = ["context", "question", "challenge"]
            kwargs["queryset"] = ContentType.objects.filter(model__in=allowed_models)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
