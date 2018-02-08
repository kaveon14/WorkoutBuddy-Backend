from django.conf.urls import url
from WBBackend.request_handlers import profile_requests
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'getProfileImage',profile_requests.getProfileImage),
    url(r'getMaxLifts',profile_requests.getMaxLifts),
    url(r'updateProfileImage',profile_requests.updateProfileImage),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

''' Things that need to be tested
-- GET Requests --

-- POST Requests --
#updateProfileImage
#getProfileImage
getMaxLifts#not testable yet

'''
