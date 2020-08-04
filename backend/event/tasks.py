from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from celery import shared_task, group, signals, uuid
from celery.contrib.abortable import AbortableTask, AbortableAsyncResult
from celery.utils.log import get_task_logger
from typing import List, Tuple, Optional
from smtplib import SMTPException

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
    task_main(check_the_list_of_events(get_list_events()))


@shared_task
def task_main(list_events):

    tasks = []

    for event in list_events:

        tasks.append(add_event_task(event))

    return group(tasks).apply_async()


@shared_task
def add_event_task(event: Tuple):

    task_id = uuid()

    return group(
        task_add_event_to_the_cache.signature(((*event[:], task_id),)),
        task_send_mail.signature((event[0],), eta=event[3], task_id=task_id)
    )


def check_the_list_of_events(list_events: List):

    filtered_list_events = []

    for event in list_events:
        if can_add_an_event(event):
            filtered_list_events.append(event)

    return filtered_list_events


def can_add_an_event(event: Tuple) -> bool:

    event_from_cache = get_event_from_the_cache(event[0])

    if event_from_cache is not None and event_from_cache[:-1] == event:
        return False

    elif event_from_cache is not None:
        abort_send_mail(event_from_cache)

    return True


def abort_send_mail(event_from_cache: List) -> None:
    abort_event_task(event_from_cache[-1])
    del_event_from_the_cache(event_from_cache[0])


def abort_event_task(task_id: str) -> None:
    result_task_send_mail = AbortableAsyncResult(task_id, app=task_send_mail)
    result_task_send_mail.abort()


@shared_task
def task_add_event_to_the_cache(event: Tuple) -> None:

    cache.set(event[0], event, timeout=(parse_datetime(event[3]) - date_now).seconds)


def get_event_from_the_cache(event_id: int) -> Optional[List]:
    event_from_cache = cache.get(event_id, None)
    if event_from_cache is not None:
        event_from_cache = *event_from_cache[0:3], parse_datetime(event_from_cache[3]), *event_from_cache[4:]
    return event_from_cache


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
        event_from_cache = get_event_from_the_cache(event_id)
        if event_from_cache is None:
            raise IndexError

        send_mail(
            f"Новое событие <<{event_from_cache[1]}>>",
            f"{event_from_cache[2]}\n{timezone.localtime(event_from_cache[3])}",
            settings.EMAIL_HOST_USER,
            [event_from_cache[4]],
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


@shared_task
def create_task_event(event_id: int):

    row_event = Event.objects.select_related('owner').get(pk=event_id)

    event = (
        row_event.id,
        row_event.title,
        row_event.description,
        row_event.event_date,
        row_event.owner.email,
    )

    if can_add_an_event(event):
        add_event_task(event).apply_async()


@shared_task
def delete_task_event(event_id: int):
    event_from_cache = get_event_from_the_cache(event_id)

    if event_from_cache is not None:
        abort_send_mail(event_from_cache)
