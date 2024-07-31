from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import *

class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email',)

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'description', 'category')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('answer_text', 'is_correct')
        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

