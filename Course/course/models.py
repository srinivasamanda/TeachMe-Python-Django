from django.contrib.auth.models import Permission, User
from django.db import models


class Course(models.Model):
    user = models.ForeignKey(User, default=1)
    author = models.CharField(max_length=250)
    course_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    course_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.course_title + ' - ' + self.author


class Notes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.chapter_title
