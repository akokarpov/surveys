# Generated by Django 4.2.3 on 2023-08-26 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=250)),
                ('required', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('radio', 'radio'), ('multi', 'multi'), ('open', 'open')], default='radio', max_length=250)),
                ('choices', models.ManyToManyField(blank=True, to='surveys.choice')),
            ],
        ),
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('self', 'self'), ('manager', 'manager'), ('peer', 'peer'), ('report', 'report')], default='self', max_length=250)),
                ('progress', models.CharField(choices=[('not started', 'not started'), ('completed', 'completed'), ('incompleted', 'incompleted')], default='not started', max_length=250)),
                ('completed_survey', models.DateTimeField(blank=True, null=True)),
                ('ratee_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratee_users', to=settings.AUTH_USER_MODEL)),
                ('rater_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rater_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('multi_rater', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('questions', models.ManyToManyField(blank=True, to='surveys.question')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='surveys.rater')),
            ],
        ),
        migrations.AddField(
            model_name='rater',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raters', to='surveys.survey'),
        ),
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.client')),
            ],
        ),
    ]
