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
