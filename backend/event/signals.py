from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from utils.utils import (
    date_now,
    date_timedelta_1_hour,
    date_timedelta_2_hours,
)
from .models import Event
from .tasks import create_task_event, delete_task_event


@receiver(pre_save, sender=Event)
def event_pre_save_signal(sender, instance, **kwargs):
    if instance.event_date <= date_now and not instance.in_archive and instance.to_repeat:
        instance.event_date += timezone.timedelta(hours=24)
    elif instance.event_date <= date_now and not instance.in_archive:
        instance.in_archive = True


@receiver(post_save, sender=Event)
def event_post_save_signal(sender, instance, created, **kwargs):
    if date_now <= instance.event_date <= date_timedelta_2_hours and not instance.in_archive:
        create_task_event(instance.pk)


@receiver(post_delete, sender=Event)
def event_post_delete_signal(sender, instance, **kwargs):
    delete_task_event(instance.pk)
