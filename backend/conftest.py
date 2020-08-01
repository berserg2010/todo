import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


root_auth = {
    'username': 'root',
    'password': 'lkasdjlkasdflaksdjf'
}


@pytest.fixture(autouse=True)
def create_superuser():
    get_user_model().objects.create_user(
        username=root_auth.get('username'),
        password=root_auth.get('password'),
    )
    yield


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
