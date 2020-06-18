from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=127,
        required=True,
    )
    description = serializers.CharField()
    event_date = serializers.DateTimeField()

    def create(self, validated_data):
        return Event.objects.create(
            validated_data['title'],
            validated_data['description'],
            validated_data['event_date'],
            # validated_data['user'],
        )

    class Meta:
        model = Event
        fields = ("id", "title", "description", "event_date")
