from django.conf.urls import url
import WorkoutBuddy.views
from WorkoutBuddy.views import CreateSubWorkout,\
    ViewDefaultExercises,ExerciseDescription,CustomExerciseDescription,SubWorkoutList,MainWorkoutList,ViewExerciseGoals

from django.conf import settings
from django.conf.urls.static import static

app_name = 'WorkoutBuddy'

urlpatterns = [
    url(r'^$', ViewDefaultExercises.as_view(), name='exercises'),
    url(r'^(?P<pk>[0-9]+)/$', ExerciseDescription.as_view(), name='exercise_description'),
    url(r'^(?P<pk>[0-9]+)/test/$', CustomExerciseDescription.as_view(), name='custom_exercise_description'),
    url(r'^createmainworkout/', WorkoutBuddy.views.createMainWorkout, name='create_mainworkout'),
    url(r'^createsubworkout/', CreateSubWorkout.as_view(), name='create_subworkout'),
    url(r'createExercise/', WorkoutBuddy.views.createExercise, name='create_exercise'),
    url(r'subworkouts/', SubWorkoutList.as_view(), name='subworkout_list'),
    url(r'mainworkouts/', MainWorkoutList.as_view(), name='mainworkout_list'),
    url(r'^(?P<pk>[0-9]+)/exercisegoals/$', ViewExerciseGoals.as_view(), name='exercise_goals'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



