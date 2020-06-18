from django.urls import path
from .views import EventCreate

urlpatterns = [
    path("",  EventCreate.as_view(), name="create_event"),
]
