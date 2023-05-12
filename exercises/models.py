from django.contrib.auth.models import User
from django.db import models

from courses.models import Classroom


class ExerciseChoices(models.Model):
    placeholder_type = [('text', 'text'), ('image', 'image'), ('voice', 'voice')]
    placeholder_type = models.CharField(choices=placeholder_type, max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
    text = models.TextField(null=True)
    voice = models.FileField(upload_to='recording/', null=True)


class Exercise(models.Model):
    choices = [('choices', 'choices'), ('words', 'words'), ('voice', 'voice')]
    text, points = models.TextField(null=True), models.FloatField(default=100)
    voice = models.FileField(upload_to='recording/', null=True)
    content_choices = models.ManyToManyField(ExerciseChoices)
    answers = models.JSONField(null=True)
    exercise_type = models.CharField(choices=choices, max_length=60)


class Lesson(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise)
    creation_date = models.DateField(auto_now_add=True)


class Assignment(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    answers, points = models.JSONField(), models.FloatField(default=0)
