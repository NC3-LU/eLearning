from django import forms
from django.utils.html import format_html


class SortingWidget(forms.Widget):
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
                <div class="row draggable-item border border-primary py-1 rounded-3" value="{c.pk}">
                    <div class="col-1 h4 align-self-center text-primary text-nowrap text-center px-0 m-0">
                        { i + 1 }.
                    </div>
                    <div class="col-10 align-self-center px-1">{ c }</div>
                    <div class="col-1 h2 align-self-center text-primary text-center px-0 m-0">
                        <i class="bi bi-grip-horizontal"></i>
                    </div>
                </div>
            """

        return html


class SortingField(forms.Field):
    def _():
        pass

    attrs = {}
    is_hidden = False
    use_required_attribute = _
    id_for_label = _

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.widget = SortingWidget(kwargs["choices"])
        self.widget.attrs = self.widget_attrs(self.widget)
        self.choices = kwargs["choices"]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        return attrs
