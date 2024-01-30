from django import forms
from django.utils.html import format_html


class SortingWidget(forms.SelectMultiple):
    class Media:
        js = (
            "npm_components/jquery-ui/dist/jquery-ui.min.js",
            "npm_components/jquery-ui-touch-punch/jquery.ui.touch-punch.min.js",
            "js/sortable.js",
        )

    choices = None

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices

    def render(self, name, value, attrs=None, renderer=None):
        rendered_html = f"""
            <div class="sortable d-grid gap-2 px-3 mx-sm-2">
                {self.get_choice_template(self.choices)}
            </div>
        """

        return format_html(rendered_html)

    def get_choice_template(self, choices):
        html = ""

        for i, c in enumerate(choices):
            html += f"""
                <div
                    class="row draggable-item border border-1
                    border-primary bg-light-blue py-1 rounded-3 small"
                    value="{c.pk}"
                    role="button">
                    <input type="checkbox" name="answer" value="{c.pk}" checked="checked"
                    class="d-none" />
                    <p class="col-1 align-self-center text-nowrap text-center px-0 m-0">
                        { i + 1 }.
                    </p>
                    <div class="col-10 align-self-center px-1">{ c }</div>
                    <div class="col-1 h2 align-self-center text-primary text-center px-0 m-0">
                        <i class="bi bi-grip-horizontal"></i>
                    </div>
                </div>
            """

        return html


class SortingField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop("queryset", None)
        temp_choices = kwargs.pop("choices", None)
        choices = kwargs["initial"] if kwargs["initial"] else temp_choices
        super().__init__(queryset, **kwargs)
        self.widget = SortingWidget(choices)
        self.widget.attrs = self.widget_attrs(self.widget)
        self.choices = choices

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        return attrs
