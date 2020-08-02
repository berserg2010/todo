from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.core.cache import cache
from celery import shared_task, group, signals, chord, uuid
from typing import List, Optional
from smtplib import SMTPException

from utils.utils import (
    date_now,
    date_timedelta_1_hour,
    date_timedelta_2_hours,
    date_timedelta_24_hours,
)
from .models import Event
from backend import settings


@signals.beat_init.connect
def task_init_in_startup(sender=None, headers=None, body=None, **kwargs):
    task_fabric()


@shared_task
def task_fabric():

    list_events = get_list_events()
    print(list_events)
    if len(list_events):
        task_adding_events_to_the_cache.s(list_events).apply_async()
        task_send_mails_delay(list_events)


@shared_task
def task_adding_events_to_the_cache(list_events: List[List]) -> None:
    group(adding_event_to_the_cache(event) for event in list_events)

def adding_event_to_the_cache(event: List) -> None:
    cache.set(event[0], event[1:], timeout=(event[3] - date_now).seconds)


def task_send_mails_delay(list_events: List[List]) -> None:
    for i in list_events:
        task_send_mail.apply_async((i, ), eta=i[3])

@shared_task
def task_send_mail(event: List) -> None:

    try:
        send_mail(
            f"Новое событие <<{event[1]}>>",
            f"{event[2]}\n{event[3]}",
            settings.EMAIL_HOST_USER,
            [event[4]],
        )
    except SMTPException as e:
        print(e)
    else:
        Event.objects.get(pk=event[0]).update_state_event_after_send_mail()


def get_list_events() -> List[Optional[List]]:
    return list(Event.objects.filter(
        in_archive=False,
        # event_date__range=(date_timedelta_1_hour, date_timedelta_2_hours),
        event_date__range=(date_now, date_timedelta_2_hours),
    ).values_list(
        'id', 'title', 'description', 'event_date', 'owner__email',
    ))


# @shared_task
# def task_to_execute_the_events():
#     pass
#
#
# @shared_task
# def task_remote_event_in_cache():
#     pass
#
#
# @shared_task
# def task_add_cache():
#     pass
#
#
# @shared_task
# def task_add_event_beat_2_hours():
#     pass