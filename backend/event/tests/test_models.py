import pytest
from mixer.backend.django import mixer

from utils.utils import (
    date_now,
    date_timedelta_2_hours,
    date_timedelta_24_hours,
    check_data,
    join_test_data,
)
from ..models import Event


pytestmark = pytest.mark.django_db


class TestEventModel:

    def test_model(self):
        instance = mixer.blend(Event)
        assert instance


    @pytest.mark.parametrize(
        'event_date, in_archive, to_repeat, correct_event_date, correct_in_archive, correct_to_repeat',
        join_test_data(
            check_data=check_data,
            correct_value=(
                (date_timedelta_2_hours, False, False,),
                (date_timedelta_2_hours, True, False,),
                (date_timedelta_2_hours, False, True,),
                (date_timedelta_2_hours, True, True,),
                (date_now, True, False),
                (date_now, True, False),
                (date_timedelta_24_hours, False, True),
                (date_now, True, True),
    )))
    def test_save(self,
            event_date, in_archive, to_repeat,
            correct_event_date, correct_in_archive, correct_to_repeat):

        instance = mixer.blend(
            Event,
            event_date=event_date,
            in_archive=in_archive,
            to_repeat=to_repeat,
        )

        assert Event.objects.get(pk=instance.pk).event_date == correct_event_date
        assert Event.objects.get(pk=instance.pk).in_archive == correct_in_archive
        assert Event.objects.get(pk=instance.pk).to_repeat == correct_to_repeat


    @pytest.mark.parametrize(
        'event_date, to_repeat, correct_event_date, correct_in_archive, correct_to_repeat',
        join_test_data(
            check_data=(
                (date_now, True, ),
                (date_now, False, ),
            ),
            correct_value=(
                (date_timedelta_24_hours, False, True),
                (date_now, True, False),
    )))
    def test_update_state_event_after_send_mail(self,
            event_date, to_repeat,
            correct_event_date, correct_in_archive, correct_to_repeat):

        instance = mixer.blend(
            Event,
            event_date=event_date,
            in_archive=False,
            to_repeat=to_repeat,
        )

        instance.update_state_event_after_send_mail()

        assert Event.objects.get(pk=instance.pk).event_date == correct_event_date
        assert Event.objects.get(pk=instance.pk).in_archive == correct_in_archive
        assert Event.objects.get(pk=instance.pk).to_repeat == correct_to_repeat
