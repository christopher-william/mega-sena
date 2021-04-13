from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Game(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    numbers = ArrayField(models.IntegerField(blank=False, null=False),
                         max_length=10, blank=False, null=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
