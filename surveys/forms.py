
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Response

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import datetime, timezone

class SurveyPageForm(forms.Form):

    def __init__(self, survey, rater, *args, **kwargs):
        super().__init__(*args, **kwargs)

        responses = Response.objects.all().filter(rater__survey_id=survey.id, rater__id=rater.id)
        questions = survey.pages.get(number=rater.survey_page_number).questions.all()

        for question in questions:
            
            choices = [(choice.id, choice.label) for choice in question.choices.all()]
            error_messages = {'required': 'This question is required!'}
            question_label = question.label
            selected_choice_id = None
            text = ""

            if rater.survey_progress == "incompleted":
                try:
                    response = responses.get(rater_id=rater.id, question_id=question.id)
                    if response.choice:
                        selected_choice_id = response.choice.id
                    if response.multichoices.all():
                        selected_choice_id = [choice.id for choice in response.multichoices.all()]
                    if response.text:
                        text = response.text
                except ObjectDoesNotExist:
                    pass
            
            if question.required:
                question_label = f"{question.label}*"                

            if question.type == 'radio':
                self.fields[f'radio_{question.id}'] = forms.ChoiceField(widget=forms.RadioSelect, choices=choices, required=question.required, label=question_label, initial=selected_choice_id, error_messages=error_messages)
            elif question.type == 'multi':
                self.fields[f'multi_{question.id}'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices, required=question.required, label=question_label, error_messages=error_messages, initial=selected_choice_id)
            elif question.type == 'open':
                self.fields[f'open_{question.id}'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '1000 symbols max.'}), max_length=1000, required=question.required, label=question_label, initial=text, error_messages=error_messages)

# class CustomAuthenticationForm(AuthenticationForm):
#     email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = User
#         fields = ('email', 'password1', 'password2')

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"
 
class DateTimeLocalField(forms.DateTimeField):
    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N 
    # is True, the locale-dictated format will be applied 
    # instead of settings.DATETIME_INPUT_FORMATS.
    # See also: 
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Date_and_time_formats
     
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

class UploadFileForm(forms.Form):
    file = forms.FileField()


class SurveySettingsForm(forms.Form):
    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['active'] = forms.BooleanField(initial=survey.active)
        self.fields['hide_raters'] = forms.BooleanField(initial=survey.hide_raters)