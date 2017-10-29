from django.conf.urls import url
import WorkoutBuddy.views
from WorkoutBuddy.views import CreateMainWorkout,CreateSubWorkout,\
    ViewDefaultExercises,ExerciseDescription,CustomExerciseDescription

from django.conf import settings
from django.conf.urls.static import static

app_name = 'WorkoutBuddy'

urlpatterns = [
    url(r'^$', ViewDefaultExercises.as_view(), name='exercises'),
    url(r'^(?P<pk>[0-9]+)/$', ExerciseDescription.as_view(), name='exercise_description'),
    url(r'^(?P<pk>[0-9]+)/test/$', CustomExerciseDescription.as_view(), name='custom_exercise_description.html'),
    url(r'^createmainworkout/', CreateMainWorkout.as_view(), name='create_mainworkout'),
    url(r'^createsubworkout/', CreateSubWorkout.as_view(), name='create_subworkout'),
    url(r'createExercise/', WorkoutBuddy.views.CreateExercise, name='create_exercise'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



