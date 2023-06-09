from django.db import models
from quizes.models import Quiz
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    submissionTime = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.quiz.name}: {self.user} - {self.score}"

class Response(models.Model):
    quiz = models.CharField(max_length=500)
    question = models.CharField(max_length=500)
    correct = models.IntegerField()

class QuizDetailedResults(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answered = models.CharField(max_length=200, default='N/A')
    correct = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.quiz.name}: {self.user} - {self.question}: {self.answered},  {self.correct}'