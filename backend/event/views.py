from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backend import settings
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner


def task_send_new_event(obj, data):

    send_mail(
        f"Новое событие <<{data.get('title')}>>",
        f"{data.get('description')}\n{data.get('event_date')}",
        settings.EMAIL_HOST_USER,
        [obj.request.user.email],
    )


def task_send_a_reminder():
    pass


class EventViewSet(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):

        task_send_new_event(self, serializer.validated_data)

        serializer.save(owner=self.request.user)
