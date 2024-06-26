from uuid import UUID

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import BooleanField, Case, IntegerField, Value, When

from .widgets import ButtonRadioSelect, SortingOptions


class AnswerForm(forms.Form):
    answer = None

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        user = kwargs.pop("user", None)
        answer_choices = (
            question.answer_choices.filter(questionanswerchoice__question=question)
            .order_by("questionanswerchoice__index")
            .annotate(
                is_correct=Case(
                    When(questionanswerchoice__is_correct=True, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        )
        initial_values = None
        if question.answer_set.filter(user=user).exists():
            user_answer = question.answer_set.get(user=user)
            initial_values = user_answer.answer_choices.all()
            if question.q_type == "SR":
                user_answer_choices = user_answer.answer_choices.through.objects.filter(
                    answer=user_answer.id
                ).order_by("id")
                user_answer_choices_ids = user_answer_choices.values_list(
                    "answerchoice_id", flat=True
                )

                ordered_user_answer_choices = (
                    question.answer_set.get(user=user)
                    .answer_choices.filter(id__in=user_answer_choices_ids)
                    .order_by(
                        Case(
                            *[
                                When(id=id_, then=pos)
                                for pos, id_ in enumerate(user_answer_choices_ids)
                            ],
                            default=Value(len(user_answer_choices_ids)),
                            output_field=IntegerField(),
                        )
                    )
                )
                initial_values = ordered_user_answer_choices

        super().__init__(*args, **kwargs)

        if question:
            self.fields["answer"] = None

            match question.q_type:
                case "S":
                    self.fields["answer"] = forms.ModelChoiceField(
                        queryset=answer_choices,
                        widget=forms.RadioSelect(),
                        required=True,
                        initial=initial_values.first() if initial_values else None,
                    )

                case "M":
                    self.fields["answer"] = forms.ModelMultipleChoiceField(
                        queryset=answer_choices,
                        widget=forms.CheckboxSelectMultiple(),
                        required=True,
                        initial=initial_values if initial_values else None,
                    )
                case "SO":
                    self.fields["answer"] = forms.ModelChoiceField(
                        queryset=answer_choices,
                        widget=forms.Select(),
                        required=True,
                    )
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
                case "SR":
                    self.fields["answer"] = forms.ModelMultipleChoiceField(
                        queryset=answer_choices,
                        widget=SortingOptions(),
                        required=True,
                        initial=initial_values if initial_values else None,
                    )
                case "LI":
                    self.fields["answer"] = forms.ModelChoiceField(
                        queryset=answer_choices,
                        widget=ButtonRadioSelect(),
                        required=True,
                        initial=initial_values.first() if initial_values else None,
                    )
                case _:
                    self.fields["answer"] = forms.CharField(
                        widget=forms.MultipleHiddenInput(),
                    )

            self.fields["answer"].widget.attrs.update(
                {"id": f"question_{question.pk}_answer"}
            )

            self.id = question.pk
            self.quiz = (
                question.quiz_set.first() if question.quiz_set.exists() else None
            )
            self.display_quiz_label = (
                question.quizquestion_set.first().display_quiz_label
                if question.quizquestion_set.exists()
                else None
            )

            self.question_quiz_index = (
                question.quizquestion_set.first().index
                if question.quizquestion_set.exists()
                else None
            )
            self.type = question.q_type
            self.fields["answer"].label = question.name
            self.fields["answer"].widget.attrs["class"] = "d-grid gap-2 ps-3 mb-5"


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
            if self.resource_type.index == 1:
                self.icon_class = "text-warning"
            elif self.resource_type.index == 2:
                self.icon_class = "text-primary"
            elif self.resource_type.index == 3:
                self.icon_class = "text-blue-dark"

            if self.fields["resource"].disabled:
                self.icon_class = "text-secondary"


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


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["autocomplete"] = "off"
