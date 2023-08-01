from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_otp.decorators import otp_required
from .forms import PreliminaryNotificationForm, QuestionForm, CategoryFormSet, ContactForm
from django.forms import formset_factory

from django.http import HttpResponseRedirect

from nisinp.settings import SITE_NAME

from formtools.wizard.views import SessionWizardView

@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        return redirect("admin:index")

def logout_view(request):
    logout(request)
    return redirect("login")


def terms(request):
    return render(request, "home/terms.html", context={"site_name": SITE_NAME})


def privacy(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})

def index(request):
    return render(request, "home/privacy_policy.html", context={"site_name": SITE_NAME})

def notifications(request):
    return render(request, "notification/index.html", context={"site_name": SITE_NAME})

# def declaration(request):
#     form = PreliminaryNotificationForm()
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = PreliminaryNotificationForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect("incident_list")

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = PreliminaryNotificationForm()

#     return render(request, "notification/declaration.html", context={"site_name": SITE_NAME, "form": form})

def incident_list(request):
    return render(request, "notification/incident_list.html", context={"site_name": SITE_NAME})

# initialize data
def get_form_list(request, form_list=None):
    return FormWizardView.as_view(form_list=PreliminaryNotificationForm.get_number_of_question())(request)


# Wizard to manage the form
class FormWizardView(SessionWizardView):

    template_name = "notification/declaration.html"
    
    def __init__(self, **kwargs):
        self.form_list = kwargs.pop('form_list')
        return super(FormWizardView, self).__init__(**kwargs)
    
    
    def get_context_data(self, form, **kwargs):
        data = self.get_cleaned_data_for_step(
            self.get_prev_step(self.steps.current))

        position = int(self.steps.current)
        if position > 0:
            # create the form with the correct question/answers
            form = CategoryFormSet.add_questions(position=position-1)

        context = super(FormWizardView, self).get_context_data(
                form=form,
                **kwargs
            )
        return context
    
    def done(self, form_list, **kwargs):
        # return render(self.request, 'incident_list', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })
        return HttpResponseRedirect("incident_list")