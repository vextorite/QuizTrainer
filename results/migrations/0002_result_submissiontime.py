# Generated by Django 4.0.6 on 2023-03-02 15:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='submissionTime',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]