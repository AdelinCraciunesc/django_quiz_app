from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

# User model with custom manager and fields so we can login with email
class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

# Quiz model with fields for name and description and user that created it
# TODO add dynamic timer
class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
# Category model with fields for name
class Category(models.Model):
    name = models.CharField(max_length=100)

    # override the __str__ method to return the name instead of the object
    def __str__(self):
        return self.name

# Question model with fields for quiz and question text
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    score = models.IntegerField(default=1)

# Answer model with fields for question and answer text and whether it is correct
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()

class User_Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
