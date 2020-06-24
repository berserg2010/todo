from __future__ import absolute_import, unicode_literals

from django.core.cache import cache
from celery import shared_task, group, signals, chord
import os

from .models import Event
from backend import settings


# @signals.beat_init.connect
# def task_adding_workstation_ip_address_to_the_cache_at_startup(sender=None, headers=None, body=None, **kwargs):
#
#     workstations_ip_addresses = list(Event.objects.filter(is_active=True).values_list('ip_address', flat=True))
#
#     cache.set("workstations_ip_addresses", workstations_ip_addresses, timeout=None)

@shared_task
def task_print_hello():
    print("Hello")

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
