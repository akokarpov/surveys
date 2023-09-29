from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Survey, Question, Choice, Response, Client, Cohort, Rater, Page, User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(UserAdmin):
   fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
   add_fieldsets = (
      (None, {
         'classes': ('wide',),
         'fields': ('email', 'password1', 'password2'),
      }),
   )
   list_display = ['id', 'email', 'first_name', 'last_name', 'is_active']
   search_fields = ['email', 'first_name', 'last_name']
   ordering = ['-date_joined']

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'client']
   list_editable = ['name']

class CohortInline(admin.TabularInline):
    model = Cohort

@admin.register(Client)
class SurveyAdmin(admin.ModelAdmin):
   list_display = ['id', 'name']
   list_editable = ['name']
   inlines = [CohortInline]

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'start_date', 'end_date', 'multi_rater', 'active']
   save_as = True

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
   list_display = ['id', 'rater', 'question', 'choice', 'text', 'added']
   ordering = ['-id']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
   list_display = ['id', 'label', 'required', 'type']
   list_editable = ['label', 'required', 'type']
   # filter_horizontal = ('choices',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
   list_display = ['id', 'label']
   list_editable = ['label']

@admin.register(Rater)
class SurveyAdmin(admin.ModelAdmin):
   list_display = ['id', 'rater_user', 'ratee_user', 'type', 'survey', 'survey_progress', 'cohort']
   list_editable = ['survey_progress']

@admin.register(Page)
class ChoiceAdmin(admin.ModelAdmin):
   list_display = ['id', 'title', 'number']
   list_editable = ['title', 'number']