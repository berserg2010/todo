import pytest
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
import datetime as dt
from django.utils.timezone import get_current_timezone

from event.models import Event
from event.tasks import (
    task_adding_events_to_the_cache_at_startup
)


pytestmark = pytest.mark.django_db


@pytest.fixture
def get_owner():
    return mixer.blend(get_user_model())


@pytest.fixture
def get_event():

    def _get_event(owner):
        return Event.objects.create(
            title="Test",
            event_date=dt.datetime.now(tz=get_current_timezone()) + dt.timedelta(hours=1.5),
            owner=owner,
        )

    return _get_event


class TestEvent:

    def test_adding_events_to_the_cache_at_startup(self, get_event, get_owner):

        owner = get_owner
        get_event(owner)
        get_event(owner)

        assert len(task_adding_events_to_the_cache_at_startup()) == 2
