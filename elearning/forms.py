import uuid

from django import forms


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
                uuid.UUID(str(user_uuid))
            except ValueError:
                raise forms.ValidationError("Invalid UUID format.")
        return user_uuid
