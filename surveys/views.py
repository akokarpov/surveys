
import re
import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import TemplateView, ListView

from .models import Survey, Rater, Response
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
            for field_name, value in request.POST.items():
                if re.search('(radio_)\d+', field_name):
                        data = {
                            'rater_id': rater_id,                     
                            'question_id': field_name[6:],
                            'choice_id': value,
                            'text': '',
                        }
                elif re.search('(multi_)\d+', field_name):
                    data = []
                    for choice in value:
                        data.append(
                            {
                        'rater_id': rater_id,                     
                        'question_id': field_name[6:],
                        'choice_id': choice,
                        'text': '',
                    }
                    )
                elif re.search('(open_)\d+', field_name):
                    data = {
                        'rater_id': rater_id,                     
                        'question_id': field_name[5:],
                        'choice_id': None,
                        'text': value,
                    }
                else:
                    data = None
                if data:
                    if type(data) == list:
                        for entry in data:
                            Response.objects.update_or_create(rater_id=entry['rater_id'], question_id=entry['question_id'], defaults=entry)
                    elif type(data) == dict:
                        Response.objects.update_or_create(rater_id=data['rater_id'], question_id=data['question_id'], defaults=data)
                    rater.survey_progress = 'incompleted'
                    rater.save()
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