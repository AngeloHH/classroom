from django.urls import path, include

from courses.views import ClassroomList, ClassroomDetail, ClassroomAddUser, ClassroomUserDetail, AvatarDetail
from exercises.views import LessonList, LessonDetail, ExerciseList, ExerciseDetail, ChoiceList, ChoiceDetail, \
    CompleteExercise, ScoreBoard

exercises = [
    path('', ExerciseDetail.as_view()),
    path('choices/', ChoiceList.as_view()),
    path('choices/<int:choice>/', ChoiceDetail.as_view()),
    path('complete/', CompleteExercise.as_view())
]

classroom = [
    path('', ClassroomDetail.as_view()),
    path('accounts/', ClassroomAddUser.as_view()),
    path('accounts/<int:user_id>/', ClassroomUserDetail.as_view()),
    path('lessons/', LessonList.as_view()),
    path('lessons/<int:lesson>/', LessonDetail.as_view()),
    path('lessons/<int:lesson>/exercises/', ExerciseList.as_view()),
    path('scoreboard/', ScoreBoard.as_view())
]

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/register/', include('dj_rest_auth.registration.urls')),
    path('auth/avatar/<int:pk>/', AvatarDetail.as_view()),
    path('classroom/', ClassroomList.as_view()),
    path('classroom/<int:pk>/', include(classroom)),
    path('exercises/<int:exercise>/', include(exercises)),
]
