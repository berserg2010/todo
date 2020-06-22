from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backend import settings
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner


class EventViewSet(ModelViewSet):

    # queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):

        send_mail(
            f"Новое событие <<{serializer.validated_data.get('title')}>>",
            f"{serializer.validated_data.get('description')}\n{serializer.validated_data.get('event_date')}",
            settings.EMAIL_HOST_USER,
            [ self.request.user.email ],
        )

        serializer.save(owner=self.request.user)
