# Generated by Django 4.2.3 on 2023-09-12 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0018_rename_created_response_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='data',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]