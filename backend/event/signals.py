from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Event
from .tasks import abort_send_mail


@receiver(post_save, sender=Event)
def event_save_signal(sender, instance, created, **kwargs):
    print('HEllo', instance.title)


@receiver(post_delete, sender=Event)
def event_delete_signal(sender, instance, **kwargs):
    abort_send_mail(instance.pk)
