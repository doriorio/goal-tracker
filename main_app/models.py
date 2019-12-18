from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Resolution(models.Model):
    goal = models.CharField(max_length=140)
    reason = models.CharField(max_length=200)
    time_period = models.CharField(max_length=30)
    notes = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.goal
        
