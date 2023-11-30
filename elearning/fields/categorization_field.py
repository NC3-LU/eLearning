from django import forms
from django.utils.html import format_html


class CategorizationWidget(forms.Widget):
    class Media:
        js = (
            "npm_components/jquery-ui/dist/jquery-ui.min.js",
            "js/drag-drop.js",
        )

    choices = None
    categories = None

    def __init__(self, choices, categories, *args, **kwargs):
        self.choices = choices
        self.categories = categories

    def render(self, name, value, attrs=None, renderer=None):
        rendered_html = f"""
            <div class="categorization_field row h-100">
                <div class="col-md-6">
                    <div>
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

        for i, c in enumerate(choices):
            html += f"""
                <div class="d-flex draggable-item border border-primary py-1 rounded-3">
                    <div class="flex-grow-0 h4 align-self-center text-primary text-nowrap text-center px-2 m-0">
                        { i + 1 }.
                    </div>
                    <div class="flex-fill align-self-center px-1">{ c.name }</div>
                    <div class="flex-grow-0 h2 align-self-center text-primary text-center px-2 m-0">
                        <i class="bi bi-grip-horizontal"></i>
                    </div>
                </div>
            """

        return html

    def get_category_template(self, categories):
        html = ""

        for c in categories:
            html += f"""
                <div class="col-md-12 flex-fill">
                    <div class="droppable bg-light-blue border border-primary rounded-3 p-3 mb-2">
                        <div class="pb-2 text-center w-100">
                            <h4>{ c.name }</h4>
                        </div>
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
        super().__init__()
        self.widget = CategorizationWidget(kwargs["choices"], kwargs["categories"])
        self.widget.attrs = self.widget_attrs(self.widget)
        self.choices = kwargs["choices"]
        self.categories = kwargs["categories"]
        self.validators = [self.validate]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        return attrs

    def validate(self, v):
        print(v)
        return True
