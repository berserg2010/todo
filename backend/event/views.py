from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from backend import settings
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner
from .tasks import task_send_new_event


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
