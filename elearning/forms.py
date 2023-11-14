from uuid import UUID

from django import forms


class AnswerForm(forms.Form):
    answer = forms.ModelMultipleChoiceField(
        queryset=None,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        super().__init__(*args, **kwargs)
        if question:
            match question.q_type:
                case "S":
                    self.fields["answer"].widget = forms.RadioSelect()
                case "M":
                    self.fields["answer"].widget = forms.CheckboxSelectMultiple()
                case "SO":
                    self.fields["answer"].widget = forms.Select()
                case "T":
                    self.fields["answer"] = forms.CharField(
                        required=True,
                        widget=forms.Textarea(
                            attrs={
                                "autofocus": True,
                                "placeholder": "",
                                "rows": 5,
                            }
                        ),
                    )

                case _:
                    self.fields["answer"].widget = forms.MultipleHiddenInput()

            self.fields["answer"].label = question.name
            self.fields["answer"].widget.attrs["class"] = "d-grid gap-2 ps-3 mb-5"
            self.fields["answer"].queryset = question.answer_choices.all().order_by(
                "index"
            )


class ResourceDownloadForm(forms.Form):
    resource = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=False,
        label_suffix="",
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop("initial", None)
        super().__init__(*args, **kwargs)
        if initial:
            self.resource_type = initial["resource"].resourceType
            self.fields["resource"].label = initial["resource"].name
            self.fields["resource"].widget.attrs["value"] = initial["resource"].id
            self.fields["resource"].disabled = initial["resource"].disabled


class inputUserUUIDForm(forms.Form):
    user_uuid = forms.UUIDField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex: ce053a70-5baf-419d-8976-757c59746081",
                "class": "border border-1 border-info",
            }
        ),
    )

    def clean_user_uuid(self):
        user_uuid = self.cleaned_data.get("user_uuid")
        if user_uuid:
            try:
                UUID(str(user_uuid))
            except ValueError:
                raise forms.ValidationError("Invalid UUID format.")
        return user_uuid
