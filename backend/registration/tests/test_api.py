import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


@pytest.fixture
def user_connection_api():

    def _user_connection_api(param):
        return APIClient().post(
            reverse(param[0]),
            param[1],
            format="json",
        )
    yield _user_connection_api


class TestUserRegistrationAPI:

    def test_create_user(self, user_connection_api):
        data = [
            "create_user",
            {
                "username": "ivanov",
                "email": "ivanov@gmail.ru",
                "password": "aslkjfalsdkja;sd",
            },
        ]

        response = user_connection_api(data)

        assert get_user_model().objects.count() == 1
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == data[1]["username"]
        assert response.data["email"] == data[1]["email"]
        assert "password" not in response.data


    def test_create_user_invalid_password(self, user_connection_api):
        data = [
            "create_user",
            {
                "username": "ivanov",
                "email": "ivanov@gmail.ru",
                "password": "abc",
            },
        ]
        response = user_connection_api(data)

        assert get_user_model().objects.count() == 0
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_create_user_no_password(self, user_connection_api):
        data = [
            "create_user",
            {
                "username": "ivanov",
                "email": "ivanov@gmail.ru",
                "password": "",
            },
        ]
        response = user_connection_api(data)

        assert get_user_model().objects.count() == 0
        assert response.status_code == status.HTTP_400_BAD_REQUEST