from django.conf.urls import url
from WBBackend.request_handlers import exercise_requests
from django.conf import settings
from django.conf.urls.static import static


#gonna need to get the post shit, may be dynamic
urlpatterns = [
    # still in testing phase,
    url(r'getDefaultExercises',exercise_requests.getDefaultExercises),
    url(r'getCustomExercises',exercise_requests.getCustomExercises),
    url(r'getAllExercises',exercise_requests.getAllExercises),
    url(r'createCustomExercise',exercise_requests.createCustomExercise),
    url(r'updateCustomExercise',exercise_requests.updateCustomExercise),
    url(r'updateCustomExerciseImage',exercise_requests.updateCustomExerciseImage),
    url(r'deleteCustomExercise',exercise_requests.deleteCustomExercise),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


''' Things that need to be tested

-- GET REQUESTS --
# getDefaultExercises

-- POST REQUESTS --
#getCustomExercises
#getAllExercises
#createCustomExercise
#updatCustomExercise
#updateCustomExerciseImage
#deleteCustomExercise
'''
