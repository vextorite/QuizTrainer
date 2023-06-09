# Generated by Django 4.1.4 on 2023-02-04 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("topic", models.CharField(max_length=200)),
                ("numberOfQuestions", models.IntegerField()),
                (
                    "time",
                    models.IntegerField(help_text="Duration of the quiz in Minutes"),
                ),
                (
                    "requiredScore",
                    models.IntegerField(help_text="required score to pass in %"),
                ),
            ],
        ),
    ]
