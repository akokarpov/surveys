# Generated by Django 4.2.3 on 2023-08-27 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='type',
            field=models.CharField(blank=True, choices=[('self', 'Self'), ('manager', 'Manager'), ('peer', 'Peer'), ('report', 'Report')], max_length=250),
        ),
    ]
