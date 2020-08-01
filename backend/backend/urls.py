from django.contrib import admin
from django.urls import path, include

from .api import router


urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/auth/",  include("rest_framework.urls")),

    path("api/", include(router.urls), name='api'),
]
