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
                  {self.get_choice_template(self.choices)}
                </div>
              </div>

              <div class="col-2">
              </div>

              <div class="col-5">
                <div>
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
                <div class="d-flex py-2">
                    <div class="flex-fill align-self-center px-1 border border-1 border-primary py-2 rounded-3">
                        <div class="d-flex">
                            <div class="flex-fill text-end align-self-center">
                                { c.name }
                            </div>
                            <div class="flex-grow-0 h4 align-self-center text-primary text-nowrap text-center px-2 m-0">
                                { i + 1 }.
                            </div>
                        </div>
                    </div>
                    <div class="flex-grow-0 text-primary text-center p-2 m-0">
                       <div id="left-dot-{ i + 1 }" class="position-absolute left-dot align-self-center">
                            <i class="bi bi-circle-fill" style="color: black;">{ i + 1 }</i>
                        </div>
                        <div id="right-dot-{ i + 1 }" class="position-absolute draggable-item right-dot">
                            <i class="bi bi-circle-fill primary-color" style="cursor: pointer">{ i + 1 }</i>
                        </div>
                    </div>

                    <!-- <div id="connector-{ i + 1 }" class="connector" data-value="{ i + 1 }"></div> -->
                </div>
            """

        return html

    def get_category_template(self, choices):
        html = ""

        for i, c in enumerate(choices):
            html += f"""
                <div class="d-flex py-2">
                    <div class="flex-grow-0 text-primary text-center p-2 m-0">
                        <div class="position-absolute droppable">
                            <i class="bi bi-circle-fill" style="color: black;"></i>
                        </div>
                    </div>
                    <div class="flex-fill align-self-center px-1 border border-1 border-primary py-2 rounded-3">
                        <div class="d-flex">
                            <div class="flex-grow-0 h4 align-self-center text-primary text-nowrap text-center px-2 m-0">
                                { chr(i + 1 + 64) }.
                            </div>
                            <div class="flex-fill align-self-center">
                                { c.name }
                            </div>
                        </div>
                    </div>

                    <!-- <div id="connector-{ i + 1 }" class="connector" data-value="{ i + 1 }"></div> -->
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
        self.widget = LinkingWidget(kwargs["choices"], kwargs["categories"])
        self.widget.attrs = self.widget_attrs(self.widget)
        self.choices = kwargs["choices"]
        self.categories = kwargs["categories"]

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        return attrs
