from django.conf.urls import url
from WorkoutBuddy.views import CreateMainWorkout,CreateSubWorkout,ViewDefaultExercises,ExerciseDescription

app_name = 'WorkoutBuddy'

urlpatterns = [
    url(r'^$', ViewDefaultExercises.as_view(), name='exercises'),
    url(r'^(?P<pk>[0-9]+)/$', ExerciseDescription.as_view(), name='exercise_description'),
    url(r'^createmainworkout/', CreateMainWorkout.as_view(), name='create_mainworkout'),
    url(r'^createsubworkout/', CreateSubWorkout.as_view(), name='create_subworkout'),
]