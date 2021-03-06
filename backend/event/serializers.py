from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'title', 'description', 'event_date',
            'in_archive', 'to_repeat',
        )
