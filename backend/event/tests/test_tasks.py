import pytest
from mixer.backend.django import mixer
from django_redis import get_redis_connection
from django.core.cache import cache
from datetime import datetime

from utils.utils import (
    date_timedelta_1_5_hours,
    check_data,
    join_test_data,
    list_events,
    format_as_iso8601,
)
from event.models import Event
from event.tasks import (
    get_list_events,
    task_adding_events_to_the_cache,
)


pytestmark = pytest.mark.django_db


class TestEvent:

    @pytest.mark.parametrize(
        'event_date, in_archive, to_repeat, correct_qs_count',
        join_test_data(
            check_data=check_data,
            correct_value=(
                (1,), (0,), (1,), (0,),
                (0,), (0,), (0,), (0,),
    )))
    def test_get_list_events(self, create_user, event_date, in_archive, to_repeat, correct_qs_count):

        user = create_user({
            'username': 'ivan',
            'password': 'pqoweirqpwoeri',
            'email': 'ivan@abc.com',
        })


        mixer.blend(
            Event,
            title='Test',
            event_date=event_date,
            in_archive=in_archive,
            to_repeat=to_repeat,
            owner=user,
        )

        assert len(get_list_events()) == correct_qs_count
        if len(get_list_events()):
            assert get_list_events() == list_events(event_date)


    def test_adding_events_to_the_cache(self):

        mixer.blend(
            Event,
            event_date=date_timedelta_1_5_hours,
            in_archive=False,
            to_repeat=False,
        )

        task_adding_events_to_the_cache(list_events(date_timedelta_1_5_hours))
        task_adding_events_to_the_cache([(2, 'Test2', '', date_timedelta_1_5_hours, 'ivan@abc.com')])

        assert cache.get(1) == ['Test', '', format_as_iso8601(date_timedelta_1_5_hours), 'ivan@abc.com']
        assert cache.get(2) == ['Test2', '', format_as_iso8601(date_timedelta_1_5_hours), 'ivan@abc.com']
