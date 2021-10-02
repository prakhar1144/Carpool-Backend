from django.db import models
from authapp.models import User

class Ride(models.Model):
    destination = models.CharField(max_length=100, blank=False, null=False)
    departure_time = models.DateTimeField(blank=False, null=False)
    admin = models.ForeignKey(User, related_name="rides",on_delete=models.CASCADE,  blank=False, null=False)
    members = models.ManyToManyField(User)