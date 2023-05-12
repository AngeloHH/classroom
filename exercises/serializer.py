from django.contrib.auth.models import User
from rest_framework import serializers

from courses.serializer import UserSerializer
from exercises.models import ExerciseChoices, Exercise, Lesson, Assignment


class SubExercisesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseChoices
        fields = ['id', 'text', 'placeholder_type', 'image', 'voice']


class ExerciseSerializer(serializers.ModelSerializer):
    content_choices = SubExercisesSerializer(many=True, read_only=True)
    answers = serializers.JSONField(write_only=True)

    class Meta:
        model = Exercise
        fields = ['id', 'text', 'voice', 'exercise_type', 'points', 'content_choices', 'answers']


class ExerciseDetailSerializer(ExerciseSerializer):
    answers = serializers.JSONField()


class LessonSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    creation_date = serializers.DateField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'author', 'exercises', 'creation_date']


class AssignmentSerializer(serializers.ModelSerializer):
    exercise = serializers.PrimaryKeyRelatedField(read_only=True)
    account = UserSerializer(read_only=True)
    points = serializers.FloatField(read_only=True)
    answers = serializers.JSONField(write_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'exercise', 'account', 'answers', 'points']
