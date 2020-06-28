import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


@pytest.fixture
def create_superuser():
    get_user_model().objects.create_user(
        username="root",
        password="lkasdjlkasdflaksdjf",
    )


@pytest.fixture
def api_client():

    client = APIClient()
    client.login(
        username="root",
        password="lkasdjlkasdflaksdjf",
    )
    return client


@pytest.fixture
def user_connection_api():

    def _user_connection_api(client, param):

        return client.post(
            reverse(param[0]),
            param[1],
            format="json",
        )

    yield _user_connection_api


class TestUserRegistrationAPI:

    def test_create_user_no_password(self, create_superuser, api_client, user_connection_api):

        data = [
            "users-list",
            {
                "username": "ivanov",
                "email": "ivanov@gmail.ru",
                "password": "",
            },
        ]

        response = user_connection_api(api_client, data)

        assert get_user_model().objects.count() == 1
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_create_user_invalid_password(self, create_superuser, api_client, user_connection_api):

        data = [
            "users-list",
            {
                "username": "ivanov",
                "email": "ivanov@gmail.ru",
                "password": "ssdf",
            },
        ]

        response = user_connection_api(api_client, data)

        assert get_user_model().objects.count() == 1
        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_create_user(self, create_superuser, api_client, user_connection_api):

        data = [
            "users-list",
            {
                "username": "ivanov",
                "email": "ivanov@gmail.ru",
                "password": "aslkjfalsdkja;sd",
            },
        ]

        response = user_connection_api(api_client, data)

        assert get_user_model().objects.count() == 2
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == data[1]["username"]
        assert response.data["email"] == data[1]["email"]
        assert "password" not in response.data
