from uuid import UUID

from django import forms
from django.db.models import Case, IntegerField, Value, When

from elearning.fields.categorization_field import CategorizationField
from elearning.fields.linking_field import LinkingField
from elearning.fields.sorting_field import SortingField


class AnswerForm(forms.Form):
    answer = None

    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", None)
        user = kwargs.pop("user", None)
        answer_choices = question.answer_choices.all().order_by("index")
        initial_values = None
        if question.answer_set.filter(user=user).exists():
            user_answer = question.answer_set.get(user=user)
            initial_values = user_answer.answer_choices.all()
            if question.q_type == "SR":
                user_answer_choices = user_answer.answer_choices.through.objects.filter(
                    answer=user_answer.id
                )
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
                case "CA":
                    categories = [
                        c.answer_choice_category
                        for c in answer_choices
                        if c is not None
                    ]
                    categories.sort(key=lambda x: x.id)
                    categories = [
                        c
                        for i, c in enumerate(categories)
                        if i == 0 or c.id != categories[i - 1].id
                    ]
                    self.fields["answer"] = CategorizationField(
                        choices=answer_choices,
                        categories=categories,
                    )
                case "SR":
                    self.fields["answer"] = SortingField(
                        choices=answer_choices.order_by("?"),
                        initial=initial_values if initial_values else None,
                    )
                case "LI":
                    categories = [
                        c.answer_choice_category
                        for c in answer_choices
                        if c is not None
                    ]
                    categories.sort(key=lambda x: x.id)
                    categories = [
                        c
                        for i, c in enumerate(categories)
                        if i == 0 or c.id != categories[i - 1].id
                    ]
                    self.fields["answer"] = LinkingField(
                        choices=answer_choices,
                        categories=categories,
                    )
                case _:
                    self.fields["answer"] = forms.CharField(
                        widget=forms.MultipleHiddenInput(),
                    )

            self.id = question.pk
            self.type = question.q_type
            self.fields["answer"].label = question.name
            self.fields["answer"].widget.attrs["class"] = "d-grid gap-2 ps-3 mb-5"
            self.fields["answer"].queryset = answer_choices


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
