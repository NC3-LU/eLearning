from django_otp.forms import OTPAuthenticationForm
from django import forms
from .models import Question, QuestionCategory, RegulationType, Services, Sector
from django.forms import formset_factory

class AuthenticationForm(OTPAuthenticationForm):
    otp_device = forms.CharField(required=False, widget=forms.HiddenInput)
    otp_challenge = forms.CharField(required=False, widget=forms.HiddenInput)

# just a class to pass some python check
class DummyForm(forms.Form):
    pass

# create a form for each question
class QuestionForm(forms.Form):

    label = forms.CharField(widget=forms.HiddenInput(), required=False)
    def __init__(self, *args, **kwargs):
        questions = Question.objects.all().order_by('position')
        question = questions[1]
        if 'question' in kwargs:
            question = kwargs.pop("question") 
        super(QuestionForm, self).__init__(*args, **kwargs)

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

# group the question in one formset
class CategoryFormSet():
    def add_questions(position):
        questionFormset = formset_factory(QuestionForm)
        categories = QuestionCategory.objects.all().order_by(
            'position').filter(question__is_preliminary = True).distinct()
        category = categories[position]
        question_form = questionFormset()
        question_form.forms = []
        questions = Question.objects.all().filter(category=category, is_preliminary= True)
        for question in questions:
            question_form.forms.append(QuestionForm(question=question))
        return question_form
            

# the first question for preliminary notification
class ContactForm(forms.Form):   
    company_name = forms.CharField(label="Company name", max_length=100)

    contact_lastname = forms.CharField(max_length=100)
    contact_firstname = forms.CharField(max_length=100)
    contact_title = forms.CharField(max_length=100)
    contact_email = forms.CharField(max_length=100)
    contact_telephone = forms.CharField(max_length=100)

    is_technical_the_same = forms.BooleanField(
        required = False,
        widget=forms.CheckboxInput(
           attrs={"class": "required checkbox "}
        ),
        initial = False
    )
    technical_lastname = forms.CharField(max_length=100)
    technical_firstname = forms.CharField(max_length=100)
    technical_title = forms.CharField(max_length=100)
    technical_email = forms.CharField(max_length=100)
    technical_telephone = forms.CharField(max_length=100)

    incident_reference = forms.CharField(max_length=255)
    complaint_reference = forms.CharField(max_length=255)

    def prepare_initial_value(**kwargs):
        request = kwargs.pop("request") 
        return {
                'contact_lastname' : request.user.last_name,
                'contact_firstname' : request.user.first_name,
                'contact_email' : request.user.email,
                'contact_telephone' : request.user.phone_number
            }

# prepare an array of sector and services        
def construct_services_array(root_categories):
    choices_serv = []
    for root_category in root_categories:
        choices_serv.append([root_category.id, root_category])
        for service in Services.objects.all().filter(sector=root_category):
            choices_serv.append([service.id,service])
        if(len(Sector.objects.all().filter(parent=root_category))>0):
                choices_serv += construct_services_array(Sector.objects.all().filter(parent=root_category))

    return choices_serv

# the affected services with services load from services table
class ImpactedServicesForm(forms.Form):
   
    choices_serv = construct_services_array(
        Sector.objects.all().filter(parent=None),
    )
    choices_rt = []
    for choice in RegulationType.objects.all():
            choices_rt.append([choice.id, choice])

    regulation = forms.MultipleChoiceField(
        required = True,
        choices = choices_rt,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "multiple-selection"}
        ),
    )
    affected_services = forms.MultipleChoiceField(
        required = True,
        choices = choices_serv,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "multiple-selection"}
        ),
    )

    
    
# class for the preliminary notification
class PreliminaryNotificationForm(forms.Form):

    # prepare the forms for the formset
    def get_number_of_question():
        questionFormset = formset_factory(QuestionForm)
        categories = QuestionCategory.objects.all().filter(question__is_preliminary = True).distinct()
        category_tree = [ContactForm]
        category_tree.append(ImpactedServicesForm)

        for category in categories:
            category_tree.append(questionFormset)           
        
        return category_tree



    
