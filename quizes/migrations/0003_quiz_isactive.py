# Generated by Django 4.0.6 on 2023-02-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0002_alter_quiz_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
