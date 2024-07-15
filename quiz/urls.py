from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # auth
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    # quiz
    path('quiz/<int:quiz_id>/', views.quiz_page, name='quiz_page'),
    path('your_quizzes/', views.your_quizzes, name='your_quizzes'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('edit_quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('question_add/<int:quiz_id>/', views.question_add, name='question_add'),
    path('question_delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('question_edit/<int:question_id>/', views.question_edit, name='question_edit'),
    path('take_quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
]
