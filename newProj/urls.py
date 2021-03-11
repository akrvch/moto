from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from newApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newApp.urls')),
    path('accounts/', include('allauth.urls')),
    path('auth/', obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)