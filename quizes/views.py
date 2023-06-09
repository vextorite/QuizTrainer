from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from results.models import Result, Response, QuizDetailedResults
from .models import Quiz
from django.views.generic import ListView
from questions.models import Answer, Question
import xlwt
import pandas

# Create your views here.

def submitResponse(request):
    return render(request, 'quizes/complete.html')

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'

def login_view(request):

    page_val = "login"

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Incorrect Username or Password')

    return render(request, 'quizes/auth-login.html', context={'page': page_val})

def quizView(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if (quiz.isActive):
        return render(request,'quizes/quiz.html', {'obj':quiz})
    else:
        return render(request, 'quizes/403.html')

def quizDataView(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.getQuestions():
        answers = []
        for a in q.getAnswers():
            answers.append(a.text)
        questions.append({str(q): answers})

    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })
def saveQuizView(request, pk):
    if (request.headers.get('x-requested-with') == 'XMLHttpRequest'):
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        results = []
        correctAnswer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected != '':
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score+=1
                            correctAnswer = a.text
                            #Response.objects.create(quiz=quiz, question=str(q), correct=1)
                            QuizDetailedResults.objects.create(quiz=quiz, user=user, question=q, answered = a_selected, correct=True)
                    else:
                        if a.correct:
                            correctAnswer = a.text
                            #Response.objects.create(quiz=quiz, question=str(q), correct=0)
                            QuizDetailedResults.objects.create(quiz=quiz, user=user, question=q, answered = a_selected, correct=False)
                results.append({str(q): {'correct_answer': correctAnswer, 'answered':a_selected}})
            else:
                results.append({str(q):'not answered'})
                #Response.objects.create(quiz=quiz, question=str(q), correct=0)
        #score_ = (score/quiz.numberOfQuestions)*100
        Result.objects.create(quiz=quiz, user=user, score=score)


    return render(request, 'done.html')

def resultsSummaryView(request):
    quizes = Quiz.objects.all()
    results = Result.objects.all().order_by('user')

    return render(request, 'quizes/results.html', context={'results':results, 'quizes':quizes})

def download_excel_data(request, pk):
    # content-type of response

    response = HttpResponse(content_type='application/ms-excel')

    output_filename = "'attachment; " + 'filename="'+ Quiz.objects.filter(id=pk).first().topic+'.xls"'

    #decide file name
    response['Content-Disposition'] = output_filename

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = ['Quiz', 'Topic', 'User', 'Score', 'Number of Questions','Submission Time', ]

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #get your data, from database or from a text file...
    data = Result.objects.filter(quiz_id=pk).order_by('user__username')
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.quiz.name, font_style)
        ws.write(row_num, 1, my_row.quiz.topic, font_style)
        ws.write(row_num, 2, my_row.user.username, font_style)
        ws.write(row_num, 3, my_row.score, font_style)
        ws.write(row_num, 4, my_row.quiz.numberOfQuestions, font_style)
        ws.write(row_num, 5, str(my_row.submissionTime), font_style)



    wb.save(response)
    return response

def download_perf_metrics(request):
    out_values = []

    responses = Response.objects.all()
    for r in responses:
        out_values.append([r.quiz, r.question, r.correct])
    newvals = pandas.DataFrame(out_values).groupby([0,1]).sum().reset_index().values.tolist()


    # content-type of response

    response = HttpResponse(content_type='application/ms-excel')

    #decide file name
    response['Content-Disposition'] = 'attachment; filename="Export.xls"'

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = ['Quiz', 'Question', 'Sum',]

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #get your data, from database or from a text file...
    data = newvals
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row[0], font_style)
        ws.write(row_num, 1, my_row[1], font_style)
        ws.write(row_num, 2, my_row[2], font_style)



    wb.save(response)
    return response

def download_quiz_responses(request):
    # content-type of response

    response = HttpResponse(content_type='application/ms-excel')

    #decide file name
    response['Content-Disposition'] = 'attachment; filename="Export.xls"'

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = ['Quiz', 'User', 'Question', 'Answered', 'Correct', ]

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    #get your data, from database or from a text file...
    data = QuizDetailedResults.objects.all().order_by('quiz')
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.quiz.name, font_style)
        ws.write(row_num, 1, my_row.user.username, font_style)
        ws.write(row_num, 2, my_row.question, font_style)
        ws.write(row_num, 3, my_row.answered, font_style)
        ws.write(row_num, 4, my_row.correct, font_style)

    wb.save(response)
    return response