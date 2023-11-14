from django import forms
from django.utils.html import format_html


class SortingWidget(forms.Widget):
    class Media:
        js = (
            "npm_components/jquery/dist/jquery.min.js",
            "https://code.jquery.com/ui/1.12.1/jquery-ui.js",
            "js/sortable.js",
        )

    choices = None

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices

    def render(self, name, value, attrs=None, renderer=None):
        rendered_html = f"""
            <div class="row h-100">
                <div class="col-md-12">
                    <div class="sortable">
                        {self.get_choice_template(self.choices)}
                    </div>
                </div>
            </div>
        """

        return format_html(rendered_html)

    def get_choice_template(self, choices):
        html = ""

        for i, c in enumerate(choices):
            html += f"""
                <div
                    class="draggable-item d-flex w-100 border border-primary p-2"
                    data-answer="odd"
                >
                    <div class="flex-grow-0">{ i + 1 }.&nbsp;</div>
                    <div class="flex-grow-1">{ c }</div>
                    <div class="flex-grow-0"><i class="bi bi-grip-vertical"></i></div>
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
