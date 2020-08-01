import pytest
from rest_framework import status

from ..models import Event


pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("create_superuser")
class TestEventsAPI:

    def test_create_user_bad_password(self, api_client_register, api_connection):

        assert Event.objects.count() == 0

        data = {
            'title': 'Test',
            'description': 'Test test test',
            'event_date': '2020-01-08T20:00',
        }

        response = api_connection(
            api_client_register,
            '/api/events/',
            'post',
            data,
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1
