# Generated by Django 4.0.6 on 2023-03-08 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_result_submissiontime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.CharField(max_length=500)),
                ('question', models.CharField(max_length=500)),
                ('correct', models.IntegerField(max_length=1)),
            ],
        ),
    ]
