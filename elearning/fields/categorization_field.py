from django import forms
from django.utils.html import format_html


class CategorizationWidget(forms.Widget):
    class Media:
        js = (
            "npm_components/jquery/dist/jquery.min.js",
            "https://code.jquery.com/ui/1.12.1/jquery-ui.js",
            "js/drag-drop.js",
        )

    choices = None
    categories = None

    def __init__(self, choices, categories, *args, **kwargs):
        self.choices = choices
        self.categories = categories

    def render(self, name, value, attrs=None, renderer=None):
        rendered_html = f"""
            <div class="row h-100">
                <div class="col-md-6">
                    <h4>Answers</h4>
                    <div id="sortable" class="sortable">
                        {self.get_choice_template(self.choices)}
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="row h-100">
                        {self.get_category_template(self.categories)}
                    </div>
                </div>
            </div>
        """

        return format_html(rendered_html)

    def get_choice_template(self, choices):
        html = ""

        for c in choices:
            html += f"""
                <div
                    class="draggable-item d-flex w-100 border border-primary p-2"
                    data-answer="odd"
                >
                    <div class="flex-grow-0">{ c }</div>
                    <div class="flex-grow-1">Answer 1</div>
                    <div class="flex-grow-0"><i class="bi bi-grip-vertical"></i></div>
                </div>
            """

        return html

    def get_category_template(self, categories):
        html = ""

        for c in categories:
            html += f"""
                <div class="col-md-12 flex-fill">
                    <div id="even" class="droppable border border-secondary bg-secondary h-100">
                        <h4>{ c }</h4>
                    </div>
                </div>
            """

        return html


class CategorizationField(forms.Field):
    def _():
        pass

    attrs = {}
    is_hidden = False
    use_required_attribute = _
    id_for_label = _

    def __init__(self, *args, **kwargs):
        print("eee")
        print(args, kwargs)
        super().__init__()
        self.widget = CategorizationWidget(kwargs["choices"], kwargs["categories"])
        self.widget.attrs = self.widget_attrs(self.widget)
        self.choices = kwargs["choices"]
        self.categories = kwargs["categories"]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        return attrs
