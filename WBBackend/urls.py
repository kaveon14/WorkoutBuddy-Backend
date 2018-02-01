from django.conf.urls import url
import WBBackend.views
from WBBackend.views import CreateSubWorkout,\
    ViewDefaultExercises,ExerciseDescription,CustomExerciseDescription,SubWorkoutList,MainWorkoutList,ViewExerciseGoals,\
    ProgressPhotosList, ViewProgressPhotos, DoWorkout, S,CompleteEX

from django.conf import settings
from django.conf.urls.static import static
from WBBackend.request_handlers import workout_requests

app_name = 'WBBackend'

urlpatterns = [
    url(r'^$', ViewDefaultExercises.as_view(), name='exercises'),
    url(r'^(?P<pk>[0-9]+)/$', ExerciseDescription.as_view(), name='exercise_description'),
    url(r'^(?P<pk>[0-9]+)/test/$', CustomExerciseDescription.as_view(), name='custom_exercise_description'),
    url(r'^createmainworkout/', WBBackend.views.createMainWorkout, name='create_mainworkout'),
    # change this back
    url(r'^createsubworkout/', DoWorkout.as_view(), name='create_subworkout'),
    # /*****/
    url(r'createExercise/', WBBackend.views.createExercise, name='create_exercise'),
    url(r'subworkouts/', SubWorkoutList.as_view(), name='subworkout_list'),
    url(r'mainworkouts/', MainWorkoutList.as_view(), name='mainworkout_list'),
    url(r'^(?P<pk>[0-9]+)/exercisegoals/$', ViewExerciseGoals.as_view(), name='exercise_goals'),
    url(r'createProgressPhoto/', WBBackend.views.createProgressPhoto, name='create_progress_photo'),
    url(r'progressphotos/',ProgressPhotosList.as_view(), name='progress_photo_list'),
    url(r'^(?P<pk>[0-9]+)/progress_photo/$', ViewProgressPhotos.as_view(), name='progress_photo'),

    #just for creating shit to test
    url(r'set/', workout_requests.createSubWorkout(),name='create_subworkout'),
    url(r'ex/',CompleteEX.as_view(),name='create_subworkout'),
    url(r'dw/',DoWorkout.as_view(),name='create_subworkout'),
    # /******/
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



