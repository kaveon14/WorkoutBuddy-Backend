from django.conf.urls import url
from WBBackend.request_handlers import exercise_requests
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^getDefaultExercises',exercise_requests.getDefaultExercises),
    url(r'^getDefaultExercise',exercise_requests.getDefaultExercise),
    url(r'^getCustomExercise',exercise_requests.getCustomExercise),
    url(r'^getCustomExercises',exercise_requests.getCustomExercises),
    url(r'^getAllExercises',exercise_requests.getAllExercises),
    url(r'^createCustomExercise',exercise_requests.createCustomExercise),
    url(r'^updateCustomExercise',exercise_requests.updateCustomExercise),
    url(r'^deleteCustomExercise',exercise_requests.deleteCustomExercise),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
