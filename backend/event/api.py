from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone

from backend import settings
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOwner

from utils.utils import (
    date_now,
    date_timedelta_1_hour,
    date_timedelta_2_hours,
    format_as_iso8601,
)


def check_event_date_in_request(req):
    if req.data.get('event_date') is not None:
        event_date = timezone.datetime.strptime(req.data.get('event_date'), '%Y-%m-%dT%H:%M:%S.%f%z')
        if date_now <= event_date <= date_timedelta_1_hour:
            print('date_now', date_now)
            print('event_date', event_date)

class EventViewSet(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):

        # task_send_new_event(self, serializer.validated_data)

        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        check_event_date_in_request(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, *args, **kwargs):
        check_event_date_in_request(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, pk=None, *args, **kwargs):
        check_event_date_in_request(request)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
