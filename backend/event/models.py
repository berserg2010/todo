from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Event(models.Model):

    title = models.CharField(max_length=127, null=False, blank=False)
    description = models.TextField(null=True, blank=True, default='')
    event_date = models.DateTimeField(null=False, blank=False)

    in_archive = models.BooleanField(null=False, blank=True, default=False)
    to_repeat = models.BooleanField(null=False, blank=True, default=False)

    owner = models.ForeignKey(
        get_user_model(),
        related_name='events',
        on_delete=models.CASCADE,
        null=False, blank=False,
    )

    def update_state_event_after_send_mail(self):
        if not self.to_repeat:
            self.in_archive = True
        self.save()

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return f'{self.title} | {self.owner} | {timezone.localtime(self.event_date)}'
