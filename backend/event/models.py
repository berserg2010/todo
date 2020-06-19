from django.db import models
from django.contrib.auth import get_user_model


class Event(models.Model):

    title = models.CharField(max_length=127, null=None, blank=None)
    description = models.TextField()
    event_date = models.DateTimeField(null=None, blank=None)

    owner = models.ForeignKey(
        get_user_model(),
        related_name="events",
        on_delete=models.CASCADE,
        null=None, blank=None,
    )

    class Meta:
        ordering = ["event_date"]
