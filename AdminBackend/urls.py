from django.contrib import admin
from django.contrib.auth import views as auth_views
from AdminBackend import views as core_views
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from .views import ApiEndpoint
from .views import secret_page

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/hello', ApiEndpoint.as_view()),
    url(r'^secret$', secret_page, name='secret'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^login', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^exercises/', include('WBBackend.urls')),
    url(r'^testExerciseApi/',include('WBBackend.request_api.exercise_urls')),
    url(r'^testWorkoutApi/',include('WBBackend.request_api.workout_urls')),
    url(r'^testProgressPhotoApi/',include('WBBackend.request_api.progress_photo_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)