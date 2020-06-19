from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from registration.views import UserViewSet
from event.views import EventViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"events", EventViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    path("api-auth/", include("rest_framework.urls")),

    path("api/", include(router.urls)),
]
