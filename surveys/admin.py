from django.contrib import admin
from .models import Survey, Question, Choice, Response, Client, Cohort, Rater, Page

# @admin.register(Cohort)
# class CohortAdmin(admin.ModelAdmin):
#    list_display = ['id', 'name', 'client']
#    list_editable = ['name']

# class CohortInline(admin.TabularInline):
#     model = Cohort

# @admin.register(Client)
# class SurveyAdmin(admin.ModelAdmin):
#    list_display = ['id', 'name']
#    list_editable = ['name']
#    inlines = [CohortInline]

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'start_date', 'end_date', 'multi_rater', 'active']
    list_editable = ['name', 'slug', 'active']
    prepopulated_fields = {'slug': ('name',)}
    save_as = True

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
   list_display = ['id', 'rater', 'question', 'choice', 'text', 'added']
   ordering = ['-id']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
   list_display = ['id', 'label', 'required', 'type']
   list_editable = ['label', 'required', 'type']
   filter_horizontal = ('choices',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
   list_display = ['id', 'label']
   list_editable = ['label']

@admin.register(Rater)
class SurveyAdmin(admin.ModelAdmin):
   list_display = ['id', 'rater_user', 'ratee_user', 'type', 'survey', 'survey_progress', 'survey_page_number',  'survey_date_taken']
   # list_editable = ['rater_user', 'ratee_user', 'type', 'survey_progress', 'survey_page_number', 'survey_date_taken']

@admin.register(Page)
class ChoiceAdmin(admin.ModelAdmin):
   list_display = ['id', 'title', 'number']
   list_editable = ['title', 'number']