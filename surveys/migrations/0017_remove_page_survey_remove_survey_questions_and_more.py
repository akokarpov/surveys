# Generated by Django 4.2.3 on 2023-09-04 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0016_alter_rater_survey_page_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='questions',
        ),
        migrations.AddField(
            model_name='survey',
            name='pages',
            field=models.ManyToManyField(blank=True, to='surveys.page'),
        ),
    ]