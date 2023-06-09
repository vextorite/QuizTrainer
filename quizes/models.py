from django.db import models
import random

# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    numberOfQuestions = models.IntegerField()
    time = models.IntegerField(help_text='Duration of the quiz in Minutes')
    requiredScore = models.IntegerField(help_text="required score to pass in %")
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.topic}: {self.name}"

    def getQuestions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.numberOfQuestions]

    class Meta:
        verbose_name_plural = 'Quizes'