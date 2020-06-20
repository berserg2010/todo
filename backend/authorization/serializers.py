from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # events = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name="event-detail",
    #     read_only=True,
    # )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username", "email",
            # "events",
        )
