from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


from utils.utils import (
    date_now,
    date_timedelta_1_hour,
    date_timedelta_2_hours,
    date_timedelta_24_hours,
)
# from .tasks import (
#     create_task_event,
#     abort_send_mail,
# )


class Event(models.Model):

    title = models.CharField(max_length=127, null=False, blank=False)
    description = models.TextField(null=True, blank=True, default="")
    event_date = models.DateTimeField(null=False, blank=False)

    in_archive = models.BooleanField(null=False, blank=True, default=False)
    to_repeat = models.BooleanField(null=False, blank=True, default=False)

    owner = models.ForeignKey(
        get_user_model(),
        related_name="events",
        on_delete=models.CASCADE,
        null=False, blank=False,
    )


    def update_state_event_after_send_mail(self):
        if not self.to_repeat:
            self.in_archive = True
        self.save()


    def save(self, *args, **kwargs):
        if self.event_date <= date_now and not self.in_archive and self.to_repeat:
            self.event_date += timezone.timedelta(hours=24)
        elif self.event_date <= date_now and not self.in_archive:
            self.in_archive = True

        super().save(*args, **kwargs)

        # if date_now <= self.event_date <= date_timedelta_2_hours and not self.in_archive:
        #     create_task_event(self.pk)


    def delete(self, *args, **kwargs):
        # abort_send_mail(self.pk)
        super().delete(*args, **kwargs)


    class Meta:
        ordering = ["-event_date"]

    def __str__(self):
        return f"{self.title} | {self.owner} | {timezone.localtime(self.event_date)}"
