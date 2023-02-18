from django.db import models
import uuid
from django.utils import timezone
# Create your models here.


class Places(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city        = models.CharField(max_length=20)
    street      = models.CharField(max_length=20)
    state       = models.CharField(max_length=20)
    country     = models.CharField(max_length=20)
    placeId     = models.CharField(max_length=100)
    latitude    = models.FloatField(blank=True, null=True)
    longitude   = models.FloatField(blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.city} {self.street}")


class Gym(models.Model):
    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name    = models.CharField(max_length=20)
    place   = models.ForeignKey(Places, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.name}")