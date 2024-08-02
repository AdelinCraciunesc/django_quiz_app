from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
# Create your tests here.

class QuizTest(TestCase):
    # setup for each test
    def setUp(self):
        # create a test user
        self.user = User.objects.create_user(email='testuser', password='12345')
        # create a test category to associate with quiz
        self.category = Category.objects.create(name='Science')
        # create a test quiz
        self.quiz = Quiz.objects.create(name='Test Quiz', description='Test Description', user=self.user, category=self.category)

    # test quiz creation
    def test_quiz_creation(self):
        quiz = self.quiz
        # assert to verify that the quiz was created with the correct details
        self.assertEqual(quiz.name, 'Test Quiz')
        self.assertEqual(quiz.description, 'Test Description')
        self.assertEqual(quiz.user, self.user)
        self.assertEqual(quiz.category, self.category)
    
    # test question creation
    def test_question_and_answers_creation(self):
        quiz = self.quiz
        question = Question.objects.create(question_text="Test Question", quiz=quiz)
        answer1 = Answer.objects.create(answer_text="Test Answer1", question=question, is_correct=True)
        answer2 = Answer.objects.create(answer_text="Test Answer2", question=question, is_correct=False)
        # assert to test that the question was created with the correct details
        self.assertEqual(question.question_text, 'Test Question')
        self.assertEqual(question.quiz, quiz)
        # assert to test that the answers were created with the correct details
        self.assertEqual(answer1.answer_text, 'Test Answer1')
        self.assertEqual(answer1.question, question)
        self.assertEqual(answer1.is_correct, True)
        self.assertEqual(answer2.answer_text, 'Test Answer2')
        self.assertEqual(answer2.question, question)
        self.assertEqual(answer2.is_correct, False)



