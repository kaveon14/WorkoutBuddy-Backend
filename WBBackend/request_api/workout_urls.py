from django.conf.urls import url
from WBBackend.request_handlers import workout_requests
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^getMainWorkouts',workout_requests.getMainWorkouts),
    url(r'^getSubWorkout',workout_requests.getSubWorkout),
    url(r'^getAllSubWorkouts',workout_requests.getSubWorkouts),
    url(r'^getExerciseGoals', workout_requests.getSubWorkoutExerciseGoals),
    url(r'^getSingleExGoal', workout_requests.getSubWorkoutExerciseGoal),
    url(r'^getCompletedWorkouts',workout_requests.getCompletedWorkouts),
    url(r'^createMainWorkout',workout_requests.createMainWorkout),
    url(r'^createSubWorkout',workout_requests.createSubWorkout),
    url(r'^deleteMainWorkout',workout_requests.deleteMainWorkout),
    url(r'^deleteSubWorkout',workout_requests.deleteSubWorkout),
    url(r'^updateMainWorkoutName',workout_requests.updateMainWorkoutName),
    url(r'^updateSubWorkoutName',workout_requests.updateSubWorkoutName),
    url(r'^addExerciseGoals',workout_requests.addSubWorkoutExerciseGoals),
    url(r'^updateExerciseGoals',workout_requests.updateExerciseGoal),
    url(r'^deleteExerciseGoals',workout_requests.deleteSubWorkoutExerciseGoals),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)