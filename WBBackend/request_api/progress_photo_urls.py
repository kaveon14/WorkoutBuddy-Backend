from django.conf.urls import url
from WBBackend.request_handlers import progress_photo_requests
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^getProgressPhotos',progress_photo_requests.getProgressPhotos),
    url(r'^addProgressPhoto',progress_photo_requests.addProgressPhoto),
    url(r'^deleteProgressPhoto',progress_photo_requests.deleteProgressPhoto),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
Things that need to be tested

-- POST --
#getProgressPhotos
#addProgressPhotos

'''
