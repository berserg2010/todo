from django.contrib import admin
from django.urls import path, include

from .api import router


urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/auth/",  include('djoser.urls')),
    path("api/auth/",  include('djoser.urls.authtoken')),

    path("api/", include(router.urls), name='api'),
]
