from django_otp.forms import OTPAuthenticationForm
from django import forms
from .models import Question, QuestionCategory, NotificationType

class AuthenticationForm(OTPAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)

# just a class to pass some python check
class DummyForm(forms.Form):
    pass

# create a form for each question
class QuestionForm(forms.Form):

    label = forms.CharField(widget=forms.HiddenInput(), required=False)
    answers = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        questions = Question.objects.all().order_by('position')
        question = questions[0]
        if 'position' in kwargs:
            questions = Question.objects.all()
            position = kwargs.pop("position") -1
            question = questions[position]
            print(question)
        super().__init__(*args, **kwargs)

        print(question.question_type)
        print(question.label)
        self.fields['label'].label = question.label
        if question.question_type == 'MULTI':
            choices = []
            for choice in question.predifined_answers.all():
                choices.append([choice.id, choice])
            self.fields["label"] = forms.MultipleChoiceField(
                required=question.is_mandatory,
                choices=choices,
                widget=forms.CheckboxSelectMultiple(
                    attrs={"class": "multiple-selection"}
                ),
                label=question.label,
            )
        elif question.question_type == 'DATE':
            self.fields['label'] = forms.DateField(
                widget=forms.SelectDateWidget()
            )
            self.fields['label'].label = question.label


# the first question for preliminary notification
class ContactForm(forms.Form):
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
    
class PreliminaryNotificationForm(forms.Form):

    # get the question for preliminary
    def get_number_of_question():
        questions = Question.objects.all()
        question_tree = [ContactForm]
        
        for question in questions:
            question_tree.append(QuestionForm)           
        
        return question_tree



    
