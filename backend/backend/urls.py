from django.contrib import admin
from django.urls import path, include
from registration import urls as registration_urls
from event import urls as event_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/registration", include(registration_urls)),
    path("api/event", include(event_urls))
]
