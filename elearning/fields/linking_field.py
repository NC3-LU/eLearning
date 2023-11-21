from django import forms
from django.utils.html import format_html


class LinkingWidget(forms.Widget):
    class Media:
        js = (
            "npm_components/jquery-ui/dist/jquery-ui.min.js",
            "js/drag-drop.js",
            "js/connector.js",
        )

    choices = None
    categories = None

    def __init__(self, choices, categories, *args, **kwargs):
        self.choices = choices
        self.categories = categories

    def render(self, name, value, attrs=None, renderer=None):
        rendered_html = f"""
            <div class="row h-100">
              <div class="col-5">
                <div>
                  {self.get_left_choice_template(self.choices)}
                </div>
              </div>

              <div class="col-2">
              </div>

              <div class="col-5">
                <div>
                  {self.get_right_choice_template(self.categories)}
                </div>
              </div>
            </div>
        """

        return format_html(rendered_html)

    def get_left_choice_template(self, choices):
        html = ""

        for i, c in enumerate(choices):
            html += f"""
                <div
                    class="d-flex w-100 border border-primary p-2"
                    data-answer="odd"
                >
                    <div class="flex-grow-0">{ i + 1 }.&nbsp;</div>
                    <div class="flex-grow-1">{ c }</div>
                    <div class="flex-grow-0">
                        <div id="left-dot-{ i + 1 }" class="position-absolute left-dot">
                            <i class="bi bi-circle-fill" style="color: black;">{ i + 1 }</i>
                        </div>
                        <div id="right-dot-{ i + 1 }" class="position-absolute draggable-item right-dot">
                            <i class="bi bi-circle-fill" style="color: blue;">{ i + 1 }</i>
                        </div>
                    </div>
                    <!-- <div id="connector-{ i + 1 }" class="connector" data-value="{ i + 1 }"></div> -->
                </div>
            """

        return html

    def get_right_choice_template(self, choices):
        html = ""

        for i, c in enumerate(choices):
            html += f"""
                <div
                    class="d-flex w-100 border border-primary p-2"
                    data-answer="odd"
                >
                    <div class="flex-grow-0">
                        <div class="droppable" style="background-color: red; width: 50px; height: 10px">
                        </div>
                    </div>
                    <div class="flex-grow-0">{ i + 1 }.&nbsp;</div>
                    <div class="flex-grow-1">{ c }</div>
                </div>
            """

        return html


class LinkingField(forms.Field):
    def _():
        pass

    attrs = {}
    is_hidden = False
    use_required_attribute = _
    id_for_label = _

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.widget = LinkingWidget(kwargs["left_choices"], kwargs["right_choices"])
        self.widget.attrs = self.widget_attrs(self.widget)
        self.left_choices = kwargs["left_choices"]
        self.right_choices = kwargs["right_choices"]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        return attrs
