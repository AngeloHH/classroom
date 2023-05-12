import json

from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from classroom.permissions import IsAdminUserOrReadOnly, IsStaffUser
from courses.models import Classroom
from courses.serializer import UserSerializer
from exercises.computed import score_percentage
from exercises.models import Lesson, Exercise, ExerciseChoices, Assignment
from exercises.serializer import LessonSerializer, ExerciseSerializer, SubExercisesSerializer, AssignmentSerializer


class LessonList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        course = Classroom.objects.get(id=course_id)
        return Lesson.objects.filter(course=course)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('pk')
        author = self.request.user
        course = Classroom.objects.get(id=course_id)
        serializer.save(author=author, course=course)


class LessonDetail(generics.RetrieveDestroyAPIView, generics.RetrieveUpdateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object(self):
        get_object = generics.get_object_or_404
        lesson_id = self.kwargs.get('lesson')
        return get_object(Lesson, id=lesson_id)


class ExerciseList(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, request, *args, **kwargs):
        get_object = generics.get_object_or_404
        lesson_id = self.kwargs.get('lesson')
        lesson = get_object(Lesson, id=lesson_id)
        objects = Exercise.objects.filter(lesson=lesson)
        serializer = self.serializer_class
        serializer = serializer(objects, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson')
        lesson = Lesson.objects.get(id=lesson_id)
        serializer.save()
        exercise_id = serializer.data['id']
        lesson.exercises.add(exercise_id)
        return Response(serializer.data)


class ExerciseDetail(generics.RetrieveDestroyAPIView, generics.RetrieveUpdateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object(self):
        exercise_id = self.kwargs.get('exercise')
        get_object = generics.get_object_or_404
        return get_object(Exercise, id=exercise_id)


class ChoiceList(generics.ListCreateAPIView):
    queryset = ExerciseChoices.objects.all()
    serializer_class = SubExercisesSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        exercise_id = self.kwargs.get('exercise')
        exercise = Exercise.objects.get(id=exercise_id)
        serializer.save()
        choice_id = serializer.data['id']
        exercise.content_choices.add(choice_id)
        return Response(serializer.data)


class ChoiceDetail(generics.RetrieveDestroyAPIView, generics.RetrieveUpdateAPIView):
    queryset = ExerciseChoices.objects.all()
    serializer_class = SubExercisesSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object(self):
        get_object = generics.get_object_or_404
        choice_id = self.kwargs.get('choice')
        return get_object(ExerciseChoices, id=choice_id)


class CompleteExercise(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data['answers'])
        exercise_id = self.kwargs.get('exercise')
        exercise = Exercise.objects.get(id=exercise_id)

        assignment = Assignment(
            account=self.request.user,
            answers=data,
            exercise=exercise
        )
        args = exercise.answers, data, exercise.points
        assignment.points = score_percentage(*args)
        assignment.save()
        return Response(self.serializer_class(assignment).data)


class ScoreBoard(generics.ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        args = 'account__id', 'account__username', 'points'
        queryset = Assignment.objects.values('account')
        queryset = queryset.annotate(points=Sum('points'))
        queryset = queryset.values(*args)
        return Response(queryset.order_by('-points'))
