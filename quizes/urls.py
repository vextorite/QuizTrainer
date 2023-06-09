from django.urls import path
from .views import QuizListView, quizView, quizDataView, saveQuizView, login_view,submitResponse, download_quiz_responses, resultsSummaryView, download_excel_data, download_perf_metrics
from django.contrib.auth.decorators import login_required


app_name = 'quizes'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', login_required(QuizListView.as_view()), name='main-view'),
    path('resultssummary/', login_required(resultsSummaryView), name='results-summary-view'),
    path('resultsexport/<int:pk>/', download_excel_data, name='export'),
    path('metricsexport/', download_perf_metrics, name='metrics-export'),
    path('responsesexport/', download_quiz_responses, name='responses-export'),
    path('submit/', submitResponse, name='submit-response'),
    path('<int:pk>/', login_required(quizView), name='quiz-view'),
    path('<int:pk>/data/', quizDataView, name='quiz-data-view'),
    path('<int:pk>/save/', saveQuizView, name='save-view'),

]