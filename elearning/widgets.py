from django import forms
from django.template.loader import render_to_string
from django.utils.html import format_html
from import_export import widgets
from parler.models import TranslationDoesNotExist

from .settings import LANGUAGES


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


# Widget that uses choice display values in place of database values
class ChoicesWidget(widgets.Widget):
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


class ButtonRadioSelect(forms.RadioSelect):
    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        rendered_html = render_to_string(
            "django/forms/widgets/button_radio_option.html", context
        )

        return format_html(rendered_html)


class SortingOptions(forms.SelectMultiple):
    class Media:
        js = [
            "npm_components/jquery-ui/dist/jquery-ui.min.js",
            "npm_components/jquery-ui-touch-punch/jquery.ui.touch-punch.min.js",
            "js/sortable.js",
        ]

    def render(self, name, value, attrs=None, renderer=None):
        choices = (
            self.choices.field.initial
            if self.choices.field.initial
            else self.choices.queryset.order_by("?")
        )
        rendered_html = render_to_string(
            "django/forms/widgets/draggable_option.html", {"choices": choices}
        )

        return format_html(rendered_html)
