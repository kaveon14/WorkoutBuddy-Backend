from django.conf.urls import url
from WBBackend.request_handlers import workout_requests
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^getMainWorkouts',workout_requests.getMainWorkouts),
    url(r'^getSubWorkouts',workout_requests.getSubWorkouts),
    url(r'^getSubWorkoutExercises',workout_requests.getSubWorkoutExercises),
    url(r'^getCompletedWorkouts',workout_requests.getCompletedWorkouts),
    url(r'^createMainWorkout',workout_requests.createMainWorkout),
    url(r'^createSubWorkout',workout_requests.createSubWorkout),
    url(r'^deleteMainWorkout',workout_requests.deleteMainWorkout),
    url(r'^deleteSubWorkout',workout_requests.deleteSubWorkout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
-- needs to be tested --
#getMainWorkouts
#getSubWorkouts
#getSubWorkoutExercises
#getCompletedWorkouts
#createMainWorkout
createSubWorkout# must be tested differently, possibly android app or use php to send post request
'''
