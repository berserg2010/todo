from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from celery import shared_task, group, signals, chord, uuid, result
from celery.result import AsyncResult
from celery.contrib.abortable import AbortableTask, AbortableAsyncResult
from celery.utils.log import get_logger, get_task_logger
from typing import List, Tuple, Optional
from smtplib import SMTPException
import time

from utils.utils import (
    date_now,
    date_timedelta_1_hour,
    date_timedelta_2_hours,
    date_timedelta_24_hours,
)
from .models import Event
from backend import settings


logger = get_task_logger(__name__)


@signals.beat_init.connect
def task_init_in_startup(sender=None, headers=None, body=None, **kwargs):
    clear_cache()
    task_main(get_list_events())


@shared_task
def task_run_beat():
    task_main(check_for_new_events(get_list_events()))


@shared_task
def task_main(list_events):

    tasks = []

    for event in list_events:

        tasks.append(add_event_task(event))

    return group(tasks).apply_async()


@shared_task
def add_event_task(event: List):

    task_id = uuid()

    return group(
        task_add_event_to_the_cache.signature(((*event[:], task_id),)),
        task_send_mail.signature((event[0],), eta=event[3], task_id=task_id)
    )


def check_for_new_events(list_events: List):

    filtered_list_events = []

    for event in list_events:

        checked_event = check_for_new_event(event)
        if checked_event is None:
            continue

        filtered_list_events.append(checked_event)

    return filtered_list_events


def check_for_new_event(event: List):

    event_in_cache = get_event_from_the_cache(event[0])

    if event_in_cache is not None and event_in_cache[:-1] == event[1:]:
        return

    abort_send_mail(event[0])

    return event


def abort_send_mail(event_id):

    print('abort_send_mail', event_id)

    event_in_cache = get_event_from_the_cache(event_id)

    if event_in_cache is not None:
        result_task_send_mail = AbortableAsyncResult(event_in_cache[-1], app=task_send_mail)
        result_task_send_mail.abort()
        del_event_from_the_cache(event_id)


@shared_task
def task_add_event_to_the_cache(event: Tuple) -> None:

    cache.set(event[0], event[1:], timeout=(parse_datetime(event[3]) - date_now).seconds)
    # cache.set(event[0], event[1:])


def get_event_from_the_cache(event_id: int) -> Optional[List]:
    event = cache.get(event_id, None)
    if event is not None:
        event = *event[0:2], parse_datetime(event[2]), *event[3:]
    return event


def del_event_from_the_cache(event_id: int) -> None:
    return cache.delete(event_id)


def clear_cache() -> None:
    return cache.clear()


@shared_task(bind=True, base=AbortableTask)
def task_send_mail(self, event_id: int) -> None:

    if self.is_aborted():
        logger.warning('Task aborted')
        return

    try:
        event = get_event_from_the_cache(event_id)
        if event is None:
            raise IndexError

        send_mail(
            f"Новое событие <<{event[0]}>>",
            f"{event[1]}\n{timezone.localtime(event[2])}",
            settings.EMAIL_HOST_USER,
            [event[3]],
        )

    except SMTPException as e:
        logger.warning(e)

    except IndexError as e:
        logger.warning(e)
    else:
        del_event_from_the_cache(event_id)
        Event.objects.get(pk=event_id).update_state_event_after_send_mail()


def get_list_events() -> List:
    return list(Event.objects.filter(
        in_archive=False,
        # event_date__range=(date_timedelta_1_hour, date_timedelta_2_hours),
        event_date__range=(date_now, date_timedelta_2_hours),
    ).values_list(
        'id', 'title', 'description', 'event_date', 'owner__email',
    ))


def create_task_event(event_id):
    pass
