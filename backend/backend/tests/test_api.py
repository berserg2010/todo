import pytest
from rest_framework import status


pytestmark = pytest.mark.django_db


list_urls = (
    '/api/',
    # '/api/users/',
    '/api/auth/users/',
    '/api/events/',
)

@pytest.mark.parametrize('url', list_urls)
def test_get_url_no_register(url, api_client, api_client_register, api_connection):

    request = api_connection(
        api_client,
        url,
    )
    assert request.status_code == status.HTTP_401_UNAUTHORIZED

    request = api_connection(
        api_client_register,
        url,
    )
    assert request.status_code == status.HTTP_200_OK
