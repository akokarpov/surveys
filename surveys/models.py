
from django.db import models
from django.conf import settings
from django.template.defaultfilters import truncatechars

class Client(models.Model):
    name                = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Cohort(models.Model):
    name                = models.CharField(max_length=250)
    client              = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.client.name})'
    
class Choice(models.Model):
    label               = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f'{self.label}'

class Question(models.Model):

    class Type(models.TextChoices):
        RADIO           = 'radio', 'radio'
        MULTI           = 'multi', 'multi'
        OPEN            = 'open', 'open'

    label               = models.CharField(max_length=250)
    required            = models.BooleanField(default=True)
    type                = models.CharField(max_length=250, default=Type.RADIO, choices=Type.choices)
    choices             = models.ManyToManyField(Choice, blank=True)

    def __str__(self) -> str:
        return f'{self.label}'

class Survey(models.Model):
    name                = models.CharField(max_length=250)
    slug                = models.SlugField(max_length=250)
    pages               = models.ManyToManyField('Page', blank=True)
    start_date          = models.DateTimeField(blank=True, null=True)
    end_date            = models.DateTimeField(blank=True, null=True)
    multi_rater         = models.BooleanField(default=False)
    active              = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name}'

class Rater(models.Model):

    class Type(models.TextChoices):
        SELF            = 'self', 'self'
        MANAGER         = 'manager', 'manager'
        PEER            = 'peer', 'peer'
        REPORT          = 'report', 'report'
    
    class Progress(models.TextChoices):
        NOT_STARTED     = 'not started', 'not started'
        COMPLETED       = 'completed', 'completed'
        INCOMPLETED     = 'incompleted', 'incompleted'

    rater_user          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rater_users', on_delete=models.CASCADE)    
    ratee_user          = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ratee_users', on_delete=models.CASCADE)
    type                = models.CharField(max_length=250, default=Type.SELF, choices=Type.choices)
    survey              = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='raters')
    survey_progress     = models.CharField(max_length=250, default=Progress.NOT_STARTED, choices=Progress.choices)
    survey_date_taken   = models.DateTimeField(blank=True, null=True)
    survey_page_number  = models.SmallIntegerField(blank=True, null=True, default=1)

    @property
    def ratee_full_name_or_username(self):
        if self.ratee_user.first_name and self.ratee_user.last_name:
            return f"{self.ratee_user.first_name} {self.ratee_user.last_name}"
        else:
            return f"{self.ratee_user.username}"

    def __str__(self) -> str:
        return f"{self.rater_user.username} {self.ratee_user.username}'s {self.type}"

class Response(models.Model):
    rater               = models.ForeignKey(Rater, related_name='responses', on_delete=models.CASCADE)
    question            = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice              = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    text                = models.TextField(blank=True)
    added               = models.DateTimeField(auto_now_add=True)        

    def __str__(self) -> str:
        return f"{self.rater.survey.name} {self.rater.ratee_user.username}'s {self.rater.type} {self.rater.rater_user.username}"
    
    @property
    def rater_input(self):
        return truncatechars(self.text, 10)

class Page(models.Model):
    title               = models.CharField(max_length=250, blank=True)
    questions           = models.ManyToManyField(Question, blank=True)
    number              = models.SmallIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.title}"