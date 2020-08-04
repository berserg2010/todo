import pytest
from mixer.backend.django import mixer

from utils.utils import (
    check_data,
    join_test_data,
    list_events,
)
from event.models import Event
from event.tasks import (
    get_list_events,
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
