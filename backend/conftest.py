import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from mixer.backend.django import mixer

from utils.utils import root_auth


@pytest.fixture
def create_user():
    def _create_user(user_data):
        return mixer.blend(
            get_user_model(),
            username=user_data.get('username'),
            password=make_password(user_data.get('password')),
            email=user_data.get('email'),
        )
    return _create_user


@pytest.fixture(autouse=True)
def create_superuser(create_user):
    create_user(root_auth)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_register():
    client = APIClient()
    client.login(
        username=root_auth.get('username'),
        password=root_auth.get('password'),
    )
    return client


@pytest.fixture
def api_connection():
    def _api_connection(client, url, method='get', param=None):
        if param is None:
            param = {}
        return getattr(client, method)(
            url,
            param,
            format="json",
        )
    return _api_connection
