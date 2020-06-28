from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils.timezone import get_current_timezone
from celery import shared_task, group, signals, chord
import os
import datetime as dt

from .models import Event
from backend import settings


# @signals.beat_init.connect
# def task_adding_workstation_ip_address_to_the_cache_at_startup(sender=None, headers=None, body=None, **kwargs):
#
#     workstations_ip_addresses = list(Event.objects.filter(is_active=True).values_list('ip_address', flat=True))
#
#     cache.set("workstations_ip_addresses", workstations_ip_addresses, timeout=None)

@shared_task
def task_adding_events_to_the_cache_at_startup():

    timedelta = dt.timedelta(hours=1)
    dt_start = dt.datetime.now(tz=get_current_timezone()) + dt.timedelta(hours=1)
    dt_end = dt_start + timedelta

    events = list(Event.objects.filter(event_date__range=(dt_start, dt_end)).values_list("id", flat=True))
    return events


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
def task_add_event_beat_two_hours():
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
