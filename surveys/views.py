
import re
import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import TemplateView, ListView

from .models import Survey, Rater, Response, Choice
from .forms import SurveyPageForm

class IndexView(TemplateView):
    template_name = "surveys/index.html"

class ThanksView(TemplateView):
    template_name = "surveys/thanks.html"

class DashboardView(ListView):
    model = Survey
    template_name = "surveys/dashboard.html"
    
    def get_queryset(self):
        return Survey.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["surveys"] = self.get_surveys_data()
        return context
    
    def get_surveys_data(self):
        surveys = self.get_queryset()
        data = {}     
        for survey in surveys:
            if survey.raters.filter(rater_user_id=self.request.user.id) != []:
                for counter, rater in enumerate(survey.raters.filter(rater_user_id=self.request.user.id)):
                    data[f"{survey.id}_{counter}"] = {
                        'survey': survey,
                        'rater': rater,
                    }
        return data

def page_view(request, survey_id, rater_id):

    survey = get_object_or_404(Survey, id=survey_id)
    rater = get_object_or_404(Rater, id=rater_id)

    def save_response(data_items, form_valid_and_next=False):
        for field, value in data_items:
            if re.search('(radio_)\d+', field):
                if form_valid_and_next and not value == "":
                    data = None
                else:
                    data = {
                        'rater_id': rater_id,                     
                        'question_id': field[6:],
                        'choice_id': None if value == "" else value,
                        'multichoices': None,
                        'text': "",
                    }
            elif re.search('(multi_)\d+', field):
                if form_valid_and_next and not value == []:
                    data = None
                else:
                    multichoices = Choice.objects.all().filter(pk__in=request.POST.getlist(field))
                    data = {
                        'rater_id': rater_id,                     
                        'question_id': field[6:],
                        'multichoices': None if value == [] else multichoices,
                        'choice_id': None,
                        'text': "",
                        } 
            elif re.search('(open_)\d+', field):
                if form_valid_and_next and value == "":
                    data = None
                else:
                    data = {
                        'rater_id': rater_id,                     
                        'question_id': field[5:],
                        'text': value,
                        'multichoices': None,
                        'choice_id': None,
                    }
            else:
                data = None
            if data:
                try:
                    response = Response.objects.get(
                        rater_id=data['rater_id'],
                        question_id=data ['question_id']
                        )
                    response.choice_id = data['choice_id']
                    response.text = data['text']
                    response.save()
                    if data['multichoices']:
                        response.multichoices.set(data['multichoices'])
                    else:
                        response.multichoices.clear()
                except Response.DoesNotExist:
                    response = Response(
                        rater_id=data['rater_id'],
                        question_id=data ['question_id'],
                        choice_id=data['choice_id'],
                        text=data['text'])
                    response.save()
                    if data['multichoices']:
                        response.multichoices.set(data['multichoices'])
                    else:
                        response.multichoices.clear()
                if rater.survey_progress == 'not started':
                    rater.survey_progress = 'incompleted'
                    rater.save()

    if request.method == 'GET':
        if rater.survey_progress == "completed" or rater not in survey.raters.all().filter(rater_user_id=request.user.id):
            raise Http404
        if request.method == 'GET':
            if 'back' in request.GET:
                if rater.survey_page_number > 1:
                    rater.survey_page_number -= 1
                    rater.save()
    
    if request.method == 'POST':
        form = SurveyPageForm(survey, rater, request.path, request.POST)
        if form.is_valid() and 'next' in request.POST:
            save_response(form.cleaned_data.items(), form_valid_and_next=True)    
            if rater.survey_page_number == survey.pages.all().count():
                rater.survey_progress = 'completed'
                rater.survey_date_taken = datetime.datetime.now(datetime.timezone.utc)
                rater.save()
                return redirect('surveys:thanks')
            else:
                rater.survey_page_number += 1
                rater.save()
                form = SurveyPageForm(survey, rater, request.path)
        else:
            save_response(form.cleaned_data.items())
    else:
        form = SurveyPageForm(survey, rater, request.path)

    context = {'form': form, 'survey': survey, 'rater': rater}
    response = render(request, "surveys/partials/page.html", context)
    return response

def take_view(request, survey_slug, survey_id, rater_id):

    survey = get_object_or_404(Survey, id=survey_id)
    rater = get_object_or_404(Rater, id=rater_id)

    if request.method == 'GET':
        if rater.survey_progress == "completed" or rater not in survey.raters.all().filter(rater_user_id=request.user.id):
            raise Http404

    context = {'survey': survey, 'rater': rater}
    return render(request, "surveys/take.html", context)