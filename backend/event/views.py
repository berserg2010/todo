from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

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
        serializer.save(owner=self.request.user)
