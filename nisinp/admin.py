from django import forms
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from django_otp import devices_for_user
from django_otp.decorators import otp_required
from django.contrib.auth.decorators import login_required
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from parler.admin import TranslatableAdmin

from nisinp.models import Company, Sector, Services, User, Question, QuestionCategory, PredifinedAnswer, RegulationType
from nisinp.settings import SITE_NAME


# Customize the admin site
class CustomAdminSite(admin.AdminSite):
    site_header = SITE_NAME + " " + _("Administration")
    site_title = SITE_NAME

    def admin_view(self, view, cacheable=False):
        #decorated_view = otp_required(view)
        decorated_view = login_required(view)
        return super().admin_view(decorated_view, cacheable)


admin_site = CustomAdminSite()


class SectorResource(resources.ModelResource):
    id = fields.Field(
        column_name="id",
        attribute="id",
    )

    name = fields.Field(
        column_name="name",
        attribute="name",
    )

    parent = fields.Field(
        column_name="parent",
        attribute="parent",
        widget=ForeignKeyWidget(Sector, field="name"),
    )

    class Meta:
        model = Sector


@admin.register(Sector, site=admin_site)
class SectorAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ["name", "parent"]
    search_fields = ["name"]
    resource_class = SectorResource


class ServicesResource(resources.ModelResource):
    id = fields.Field(
        column_name="id",
        attribute="id",
    )

    name = fields.Field(
        column_name="name",
        attribute="name",
    )

    sector = fields.Field(
        column_name="sector",
        attribute="sector",
        widget=ForeignKeyWidget(Sector, field="name"),
    )

    class Meta:
        model = Sector


@admin.register(Services, site=admin_site)
class ServicesAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ["name", "sector"]
    search_fields = ["name"]
    resource_class = ServicesResource


class CompanyResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id")
    identifier = fields.Field(column_name="identifier", attribute="identifier")
    name = fields.Field(column_name="name", attribute="name")
    address = fields.Field(column_name="address", attribute="address")
    country = fields.Field(column_name="country", attribute="country")
    email = fields.Field(column_name="email", attribute="email")
    phone_number = fields.Field(column_name="phone_number", attribute="phone_number")
    is_regulator = fields.Field(column_name="is_regulator", attribute="is_regulator")
    monarc_path = fields.Field(column_name="monarc_path", attribute="monarc_path")
    sectors = fields.Field(
        column_name="sectors",
        attribute="sectors",
        widget=ManyToManyWidget(Sector, field="name", separator=","),
    )

    class Meta:
        model = Company


class companySectorInline(admin.TabularInline):
    model = Company.sectors.through
    verbose_name = _("sector")
    verbose_name_plural = _("sectors")
    extra = 1


@admin.register(Company, site=admin_site)
class CompanyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CompanyResource
    list_display = [
        "name",
        "address",
        "country",
        "email",
        "phone_number",
        "is_regulator",
    ]
    list_filter = ["is_regulator", "sectors"]
    search_fields = ["name"]
    filter_horizontal = ("sectors", "sectors")
    inlines = (companySectorInline,)
    fieldsets = [
        (
            _("Contact Information"),
            {
                "classes": ["extrapretty"],
                "fields": [
                    "name",
                    ("address", "country"),
                    ("email", "phone_number"),
                ],
            },
        ),
        (
            _("Permissions"),
            {
                "classes": ["extrapretty"],
                "fields": [
                    "is_regulator",
                ],
            },
        ),
        (
            _("Configuration Information"),
            {
                "classes": ["extrapretty"],
                "fields": [
                    "identifier",
                    "monarc_path",
                ],
            },
        ),
    ]


class CustomAdminForm(forms.ModelForm):
    list_companies = forms.MultipleChoiceField(
        label=_("Companies"),
        widget=forms.CheckboxSelectMultiple,
    )

    list_sectors = forms.MultipleChoiceField(
        label=_("Sectors"),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = "__all__"


class UserResource(resources.ModelResource):
    id = fields.Field(column_name="id", attribute="id")
    first_name = fields.Field(column_name="first_name", attribute="first_name")
    last_name = fields.Field(column_name="last_name", attribute="last_name")
    email = fields.Field(column_name="email", attribute="email")
    phone_number = fields.Field(column_name="phone_number", attribute="phone_number")
    companies = fields.Field(
        column_name="companies",
        attribute="companies",
        widget=ManyToManyWidget(Company, field="name", separator=","),
    )
    sectors = fields.Field(
        column_name="sectors",
        attribute="sectors",
        widget=ManyToManyWidget(Sector, field="name", separator=","),
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "companies",
            "sectors",
        ]

# reset the 2FA we delete the TOTP devices
@admin.action(description=_("Reset 2FA"))
def reset_2FA(modeladmin, request, queryset):
    for user in queryset:
        devices = devices_for_user(user)
        for device in devices:
            device.delete()


@admin.register(User, site=admin_site)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = CustomAdminForm
    resource_class = UserResource
    list_display = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_staff",
    ]
    search_fields = ["first_name", "last_name", "email"]
    list_filter = [
        "companies",
        "sectors",
        "is_staff",
    ]
    list_display_links = ("email", "first_name", "last_name")
    filter_horizontal = ("groups",)
    fieldsets = [
        (
            _("Contact Information"),
            {
                "classes": ["extrapretty"],
                "fields": [
                    ("first_name", "last_name"),
                    ("email", "phone_number"),
                ],
            },
        ),
    ]
    actions = [reset_2FA]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            fieldsets = [fs for fs in fieldsets if fs[0] != _("Permissions")]

            fieldsets.append(
                (
                    _("Companies"),
                    {
                        "classes": ["extrapretty"],
                        "fields": ["list_companies"],
                    },
                )
            )

            fieldsets.append(
                (
                    _("Sectors"),
                    {
                        "classes": ["extrapretty"],
                        "fields": ["list_sectors"],
                    },
                )
            )
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["list_companies"].required = False
        form.base_fields["list_sectors"].required = False

        if not request.user.is_superuser:
            if obj is not None:
                selected_companies = [company.id for company in obj.companies.all()]
                selected_sectors = [sector.id for sector in obj.sectors.all()]
                form.base_fields["list_companies"].initial = selected_companies
                form.base_fields["list_sectors"].initial = selected_sectors

            companies_tuples = [
                (company.id, company.name) for company in request.user.companies.all()
            ]
            form.base_fields["list_companies"].required = True
            form.base_fields["list_companies"].choices = companies_tuples

            sectors_tuples = [
                (sector.id, sector.name) for sector in request.user.sectors.all()
            ]
            form.base_fields["list_sectors"].required = True
            form.base_fields["list_sectors"].choices = sectors_tuples

        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        if request.user.has_perms(
            [
                "governanceplatform.add_user",
                "governanceplatform.change_user",
                "governanceplatform.delete_user",
            ],
        ):
            return queryset.filter(
                sectors__in=request.user.sectors.filter(
                    sectorcontact__is_sector_contact=True
                ),
                companies__in=request.user.companies.all(),
            ).distinct()
        return queryset.exclude(email=request.user.email)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            super().save_model(request, obj, form, change)

            list_companies = form.cleaned_data.get("list_companies")
            list_sectors = form.cleaned_data.get("list_sectors")

            if list_companies is not None:
                obj.companies.set(list_companies)

            if list_sectors is not None:
                obj.sectors.set(list_sectors)
        else:
            if obj.id is None and obj.is_staff:
                super().save_model(request, obj, form, change)
                obj.user_permissions.add(
                    Permission.objects.get(codename="add_user"),
                    Permission.objects.get(codename="change_user"),
                    Permission.objects.get(codename="delete_user"),
                )
            super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        for formset in formsets:
            for form in formset.forms:
                is_company_admin = form.cleaned_data.get("is_company_administrator")
                user = form.cleaned_data.get("user")

                if user is not None and request.user.is_staff:
                    user.is_staff = is_company_admin
                    user.save()

class FunctionalityResource(resources.ModelResource):
    id = fields.Field(
        column_name="id",
        attribute="id",
    )

    name = fields.Field(
        column_name="name",
        attribute="name",
    )

class PredifinedAnswerResource(resources.ModelResource):
    id = fields.Field(
        column_name="id",
        attribute="id",
    )
    predifined_answer = fields.Field(
        column_name="predifined_answer",
        attribute="predifined_answer",
    )
    allowed_additional_answer = fields.Field(
        column_name="allowed_additional_answer",
        attribute="allowed_additional_answer",
    )

    class Meta:
        model = PredifinedAnswer

@admin.register(PredifinedAnswer, site=admin_site)
class PredifinedAnswerAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ["predifined_answer", "allowed_additional_answer"]
    search_fields = ["allowed_additional_answer, predifined_answer"]
    resource_class = PredifinedAnswerResource

class QuestionCategoryResource(resources.ModelResource):
    id = fields.Field(
        column_name="id",
        attribute="id",
    )
    label = fields.Field(
        column_name="label",
        attribute="label",
    )

    class Meta:
        model = QuestionCategory

@admin.register(QuestionCategory, site=admin_site)
class QuestionCategoryAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ["label", "position"]
    search_fields = ["label"]
    resource_class = QuestionCategoryResource

class QuestionResource(resources.ModelResource):
    id = fields.Field(
        column_name="id",
        attribute="id",
    )

    label = fields.Field(
        column_name="label",
        attribute="label",
    )
    predifined_answers = fields.Field(
        column_name="predifined_answers",
        attribute="predifined_answers",
        widget=ManyToManyWidget(PredifinedAnswer, field="predifined_answer", separator=","),
    )
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ManyToManyWidget(QuestionCategory, field="label", separator=","),
    )

    class Meta:
        model = Question
        fields = "__all__"


@admin.register(Question, site=admin_site)
class QuestionAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = [
        "label",
        "category", 
        "get_predifined_answers"
    ]
    search_fields = ["label"]
    resource_class = QuestionResource

class RegulationTypeResource(resources.ModelResource):
    label = fields.Field(
        column_name="label",
        attribute="label",
    )

    class Meta:
        model = RegulationType

@admin.register(RegulationType, site=admin_site)
class RegulationTypeAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ["label"]
    search_fields = ["label"]
    resource_class = RegulationTypeResource