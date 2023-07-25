from django_otp.forms import OTPAuthenticationForm
from django import forms

class AuthenticationForm(OTPAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)

class PreliminaryNotificationForm(forms.Form):
    company_name = forms.CharField(label="Company name", max_length=100)

    # contact_lastname = forms.CharField(max_length=100)
    # contact_firstname = forms.CharField(max_length=100)
    # contact_title = forms.CharField(max_length=100)
    # contact_email = forms.CharField(max_length=100)
    # contact_telephone = forms.CharField(max_length=100)

    # technical_lastname = forms.CharField(max_length=100)
    # technical_firstname = forms.CharField(max_length=100)
    # technical_title = forms.CharField(max_length=100)
    # technical_email = forms.CharField(max_length=100)
    # technical_telephone = forms.CharField(max_length=100)

    # incident_reference = forms.CharField(max_length=255)
    # complaint_reference = forms.CharField(max_length=255)