# Generated by Django 4.2.3 on 2023-09-02 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0013_rename_order_page_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rater',
            old_name='posted_page_number',
            new_name='current_page_number',
        ),
    ]
