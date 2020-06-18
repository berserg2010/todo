from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from event.models import Event


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(
    #     max_length=32,
    #     validators=[
    #         UniqueValidator(queryset=get_user_model().objects.all())
    #     ],
    # )
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[
    #         UniqueValidator(queryset=get_user_model().objects.all())
    #     ],
    # )
    # password = serializers.CharField(
    #     min_length=8,
    #     write_only = True,
    # )
    #
    # def create(self, validated_data):
    #     return get_user_model().objects.create_user(
    #         validated_data['username'],
    #         validated_data['email'],
    #         validated_data['password'],
    #     )

    events = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all()
    )

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "events")
