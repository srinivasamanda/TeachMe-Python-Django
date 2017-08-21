from django import forms
from django.contrib.auth.models import User

from .models import Course, Notes


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['author', 'course_title', 'genre', 'course_logo']


class NotesForm(forms.ModelForm):

    class Meta:
        model = Notes
        fields = ['chapter_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
