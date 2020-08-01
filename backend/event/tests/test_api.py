import pytest
from rest_framework import status
from django.utils import timezone

from ..models import Event


pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("create_superuser")
class TestEventsAPI:

    def test_event_crud(self, api_client_register, api_connection):

        assert Event.objects.count() == 0

        data = {
            'title': 'Test',
            'description': 'Test test test',
            'event_date': timezone.now(),
        }
        response = api_connection(
            api_client_register,
            '/api/events/',
            'post',
            data,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.count() == 1

        response = api_connection(
            api_client_register,
            '/api/events/',
            'get',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0].get('title') == data.get('title')

        data = {
            'title': 'Test2',
            'description': 'Test test test',
            'event_date': timezone.now(),
        }
        response = api_connection(
            api_client_register,
            '/api/events/1/',
            'put',
            data,
        )
        assert Event.objects.get(pk=1).title == data.get('title')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('title') == data.get('title')

        data = {
            'description': 'Test test test Test test test',
        }
        response = api_connection(
            api_client_register,
            '/api/events/1/',
            'patch',
            data,
        )
        assert Event.objects.get(pk=1).description == data.get('description')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('description') == data.get('description')

        response = api_connection(
            api_client_register,
            '/api/events/1/',
            'delete',
        )
        assert Event.objects.count() == 0
        assert response.status_code == status.HTTP_204_NO_CONTENT
