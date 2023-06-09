from django.contrib import admin
from .models import Result, Response, QuizDetailedResults

# Register your models here.
admin.site.register(Result)
admin.site.register(Response)
admin.site.register(QuizDetailedResults)