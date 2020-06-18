from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import EventCreate

urlpatterns = [
    path("",  EventCreate.as_view(), name="create_event"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
