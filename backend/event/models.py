from django.db import models
from django.contrib.auth import get_user_model


class Event(models.Model):

    title = models.CharField(max_length=127)
    description = models.TextField()
    event_date = models.DateTimeField()

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
