from uuid import UUID

from django import forms


class AnswerForm(forms.Form):
    answer = None

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        print("QUESTION")
        print(vars(question))
        super().__init__(*args, **kwargs)
        if question:
            if question.q_type == "M":
                answer = forms.ModelMultipleChoiceField(
                    queryset=None,
                    required=True,
                )
                answer.label = question.name
                answer.widget = forms.CheckboxSelectMultiple()
                answer.queryset = question.answer_choices.all()
            elif question.q_type == "S":
                self.fields["answer"].widget = forms.RadioSelect()
                self.fields["answer"].queryset = question.answer_choices.all()
            elif question.q_type == "SO":
                self.fields["answer"].widget = forms.CheckboxSelectMultiple()
                self.fields["answer"].queryset = question.answer_choices.all()
            elif question.q_type == "T":
                self.fields["answer"].widget = forms.TextInput()
            elif question.q_type == "MT":
                self.fields["answer"].widget = forms.TextInput()
            elif question.q_type == "ST":
                self.fields["answer"].widget = forms.TextInput()
            elif question.q_type == "CL":
                self.fields["answer"].widget = forms.Select()
                self.fields["answer"].queryset = question.answer_choices.all()
            elif question.q_type == "CA":
                pass
            elif question.q_type == "MA":
                pass


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
