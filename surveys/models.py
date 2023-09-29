import uuid
from django.db import models
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    id                  = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False, unique=True)
    email               = models.EmailField(unique=True)
    username            = None
    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = []
    objects             = UserManager()
    

class Client(models.Model):
    name                = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Cohort(models.Model):
    name                = models.CharField(max_length=250, unique=True)
    client              = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
    
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
    id                  = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False, unique=True)
    name                = models.CharField(max_length=250)
    pages               = models.ManyToManyField('Page', blank=True)
    start_date          = models.DateTimeField(blank=True, null=True)
    end_date            = models.DateTimeField(blank=True, null=True)
    multi_rater         = models.BooleanField(default=False)
    active              = models.BooleanField(default=False)
    hide_raters         = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.name}'

class Rater(models.Model):

    class Type(models.TextChoices):
        SELF            = 'self', 'self'
        MANAGER         = 'manager', 'manager'
        PEER            = 'peer', 'peer'
        REPORT          = 'report', 'report'
    
    class Progress(models.TextChoices):
        UNSTARTED       = 'unstarted', 'unstarted'
        INCOMPLETE      = 'incomplete', 'incomplete'
        FINISHED        = 'finished', 'finished'

    id                  = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False, unique=True)
    rater_user          = models.ForeignKey(User, related_name='rater_users', on_delete=models.CASCADE)    
    ratee_user          = models.ForeignKey(User, related_name='ratee_users', on_delete=models.CASCADE)
    type                = models.CharField(max_length=250, default=Type.SELF, choices=Type.choices)
    survey              = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='raters')
    survey_progress     = models.CharField(max_length=250, default=Progress.UNSTARTED, choices=Progress.choices)
    survey_date_taken   = models.DateTimeField(blank=True, null=True)
    survey_page_number  = models.SmallIntegerField(blank=True, null=True, default=1)
    cohort              = models.ForeignKey(Cohort, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def ratee_name_or_email(self):
        if self.ratee_user.first_name and self.ratee_user.last_name:
            return f"{self.ratee_user.first_name} {self.ratee_user.last_name}"
        else:
            return f"{self.ratee_user.email}"
    
    @property
    def rater_name_or_email(self):
        if self.rater_user.first_name and self.rater_user.last_name:
            return f"{self.rater_user.first_name} {self.rater_user.last_name}"
        else:
            return f"{self.rater_user.email}"

    def __str__(self) -> str:
        return f"{self.rater_user.email} {self.ratee_user.email}'s {self.type}"

class Response(models.Model):
    rater               = models.ForeignKey(Rater, related_name='responses', on_delete=models.CASCADE)
    question            = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice              = models.ForeignKey(Choice, on_delete=models.CASCADE, blank=True, null=True)
    multichoices        = models.ManyToManyField(Choice, blank=True, related_name='multichoices')
    text                = models.TextField(blank=True)
    added               = models.DateTimeField(auto_now_add=True)        

    def __str__(self) -> str:
        return f"{self.rater.survey.name} {self.rater.ratee_user.email}'s {self.rater.type} {self.rater.rater_user.email}"
    
    @property
    def rater_input(self):
        return truncatechars(self.text, 10)

class Page(models.Model):
    title               = models.CharField(max_length=250, blank=True)
    questions           = models.ManyToManyField(Question)
    number              = models.SmallIntegerField()

    def __str__(self) -> str:
        return f"{self.title}"