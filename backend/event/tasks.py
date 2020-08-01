from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.core.cache import cache
from celery import shared_task, group, signals, chord
from typing import List

from utils.utils import (
    date_now,
    date_timedelta_2_hours,
    date_timedelta_24_hours,
)
from .models import Event
from backend import settings


# @signals.beat_init.connect
# def task_adding_workstation_ip_address_to_the_cache_at_startup(sender=None, headers=None, body=None, **kwargs):
#
#     workstations_ip_addresses = list(Event.objects.filter(is_active=True).values_list('ip_address', flat=True))
#
#     cache.set("workstations_ip_addresses", workstations_ip_addresses, timeout=None)


def get_list_events():
    return list(Event.objects.filter(in_archive=False, event_date__range=(date_now, date_timedelta_2_hours)).values_list(
        'id', 'title', 'description', 'event_date', 'owner__email',
    ))


@shared_task
def task_adding_events_to_the_cache(list_events: List):

    for i in list_events:
        cache.set(i[0], i[1:], timeout=(i[3] - date_now).seconds)


@shared_task
def task_print_hello():
    print("Hello")


@shared_task
def task_writhe_db():
    pass


@shared_task
def task_add_cache():
    pass


@shared_task
def task_add_event_beat_2_hours():
    pass


@shared_task
def task_send_new_event(obj, data):

    send_mail(
        f"Новое событие <<{data.get('title')}>>",
        f"{data.get('description')}\n{data.get('event_date')}",
        settings.EMAIL_HOST_USER,
        [obj.request.user.email],
    )


@shared_task
def task_send_a_reminder():
    pass


# @shared_task
# def task_get_data_from_workstations():
#
#     ip_addresses = cache.get("workstations_ip_addresses")
#
#     data = group(
#         task_get_wmi_objects.s(ip_address) for ip_address in ip_addresses
#     ).apply_async()
#
#     return None
#
# @shared_task
# def task_get_wmi_objects(ip_address: str):
#
#     data = (
#         group(task_get_wmi_object.s(ip_address, wmi_class) |
#         task_entering_data_into_the_wmi_model.s() for wmi_class in list_models)
#     ).apply_async()
#
#     return None
