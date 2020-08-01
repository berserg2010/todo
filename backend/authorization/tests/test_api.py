import pytest
from django.contrib.auth import get_user_model
from rest_framework import status


pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("create_superuser")
class TestUsersAPI:

    @pytest.mark.parametrize('password', ['', 'ssdf'])
    def test_create_user_bad_password(self, password, api_client_register, api_connection):

        data = {
            "username": "ivanov",
            "email": "ivanov@gmail.ru",
            "password": password,
        }

        response = api_connection(
            api_client_register,
            '/api/users/',
            'post',
            data,
        )

        assert get_user_model().objects.count() == 1
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user(self, api_client_register, api_connection):

        data = {
            "username": "ivanov",
            "email": "ivanov@gmail.ru",
            "password": "aslkjfalsdkja;sd",
        }

        response = api_connection(
            api_client_register,
            '/api/users/',
            'post',
            data,
        )

        assert get_user_model().objects.count() == 2
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == data.get("username")
        assert response.data["email"] == data.get("email")
        assert "password" not in response.data
