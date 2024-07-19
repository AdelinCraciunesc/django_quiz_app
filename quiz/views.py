from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import *
from .forms import *
# Create your views here.
@login_required(login_url='login')
def home(request):
    user = request.user
    all_quiz = Quiz.objects.all()
    return render(request, 'home.html', {'user': user, 'quizzes': all_quiz})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login') 
    return render(request, 'auth/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
    # return render(request, 'auth/register.html')

# quiz
def your_quizzes(request):
    user = request.user
    all_quizzes = Quiz.objects.filter(user=user)

    return render(request, 'quiz/your_quizzes.html', {'user': user, 'quizzes': all_quizzes})

def quiz_page(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    questions_and_answers = {}
    for question in questions:
        answers = Answer.objects.filter(question=question)
        questions_and_answers[question] = answers
    return render(request, 'quiz/quiz_page.html', {'quiz': quiz, 'questions_and_answers': questions_and_answers})

def create_quiz(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.user = request.user
            quiz.save()
            return redirect('your_quizzes')
        else:
            print(quiz_form.errors)
    else:
        quiz_form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'quiz_form': quiz_form})

def delete_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=quiz_id)
        quiz.delete()
        return redirect('your_quizzes')

def edit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=quiz_id)
        quiz_form = QuizForm(request.POST, instance=quiz)
        if quiz_form.is_valid():
            quiz_form.save()
            return redirect('your_quizzes')
        else:
            print(quiz_form.errors)
    else:
        quiz = Quiz.objects.get(id=quiz_id)
        quiz_form = QuizForm(instance=quiz)
    return render(request, 'quiz/edit_quiz.html', {'quiz_form': quiz_form})

# question
def question_add(request, quiz_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_forms = inlineformset_factory(Question, Answer, fields=('answer_text', 'is_correct'), extra=4, can_delete=False)
        answer_forms = answer_forms(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = Quiz.objects.get(id=quiz_id)
            question.save()
            for answer_form in answer_forms:
                if answer_form.is_valid():
                    answer = answer_form.save(commit=False)
                    answer.question = question
                    answer.save()
            messages.success(request, 'Question added successfully')
            return redirect('quiz_page', quiz_id=quiz_id)
        else:
            print(question_form.errors)
    else:
        question_form = QuestionForm()
        answer_forms = inlineformset_factory(Question, Answer, fields=('answer_text', 'is_correct'), extra=4, can_delete=False)
    return render(request, 'quiz/question_add.html', {'question_form': question_form, 'answer_forms': answer_forms})

def question_delete(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question)
        for answer in answers:
            answer.delete()
        question.delete()
        return redirect('quiz_page', quiz_id=question.quiz.id)
    
def question_edit(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(id=question_id)
        question_form = QuestionForm(request.POST, instance=question)
        answer_forms = inlineformset_factory(Question, Answer, fields=('answer_text', 'is_correct'), extra=4, can_delete=False)
        answer_forms = answer_forms(request.POST, instance=question, queryset=Answer.objects.filter(question=question))
        if question_form.is_valid():
            question_form.save()
            for answer_form in answer_forms:
                if answer_form.is_valid():
                    answer = answer_form.save(commit=False)
                    answer.question = question
                    answer_form.save()
            messages.success(request, 'Question edited successfully')
            return redirect('quiz_page', quiz_id=question.quiz.id)
        else:
            print(question_form.errors)
    else:
        question = Question.objects.get(id=question_id)
        question_form = QuestionForm(instance=question)
        answer_forms = inlineformset_factory(Question, Answer, fields=('answer_text', 'is_correct'), extra=4, can_delete=False, max_num=4)
        answer_forms = answer_forms(instance=question, queryset=Answer.objects.filter(question=question))
    return render(request, 'quiz/question_edit.html', {'question_form': question_form, 'answer_forms': answer_forms})

def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    questions_and_answers = {}
    for question in questions:
        answers = Answer.objects.filter(question=question)
        questions_and_answers[question] = answers
    
    if request.method == 'POST':
        score = 0
        total_score = questions.count()
        questions_correct = {}
        questions_incorrect = {}
        answered_questions = set()

        for key, value in request.POST.items():
            if key.startswith('answer_'):
                question_id = key.split('_')[1] 
                selected_option_id = value
                question = Question.objects.get(id=question_id)
                option = Answer.objects.get(id=selected_option_id)
                answered_questions.add(question_id)

                if option.is_correct:
                    score += 1
                    questions_correct[question] = option
                else:
                    questions_incorrect[question] = option
        for question in questions:
            if str(question.id) not in answered_questions:
                questions_incorrect[question] = None

        user = request.user
        user_result = User_Result.objects.create(user=user, quiz=quiz, score=score)
        user_result.save()

        return render(request, 'quiz/quiz_result.html', 
                      {'score': score,
                       'total_score': total_score,
                       'questions_correct': questions_correct, 
                       'questions_incorrect': questions_incorrect})
    
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions_and_answers': questions_and_answers})
