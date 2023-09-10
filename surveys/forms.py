
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Response

class SurveyPageForm(forms.Form):

    def __init__(self, survey, rater, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        responses = Response.objects.all().filter(rater__survey_id=survey.id, rater__id=rater.id)
        questions = survey.pages.get(number=rater.survey_page_number).questions.all()

        for question in questions:
            
            choices = [(choice.id, choice.label) for choice in question.choices.all()]
            error_messages = {'required': 'This is a mandatory question to answer.'}
            attrs = {"hx-post": f"{path}", "hx-trigger": "change", "novalidate": True}
            question_label = question.label
            selected_choice_id = None
            text = ""

            if rater.survey_progress == "incompleted":
                try:
                    response = responses.get(rater_id=rater.id, question_id=question.id)
                    if response.choice:
                        selected_choice_id = response.choice.id
                    if response.text:
                        text = response.text
                except ObjectDoesNotExist:
                    pass
            
            if question.required:
                question_label = f"{question.label}*"                

            if question.type == 'radio':
                self.fields[f'radio_{question.id}'] = forms.ChoiceField(widget=forms.RadioSelect(attrs=attrs), choices=choices, required=question.required, label=question_label, initial=selected_choice_id, error_messages=error_messages)
            elif question.type == 'multi':
                self.fields[f'multi_{question.id}'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs=attrs), choices=choices, required=question.required, initial=selected_choice_id, label=question_label, error_messages=error_messages)
            elif question.type == 'open':
                self.fields[f'open_{question.id}'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '1000 symbols max.', **attrs}), max_length=1000, required=question.required, label=question_label, initial=text, error_messages=error_messages)