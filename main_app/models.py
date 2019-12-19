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
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

class Comemnt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_at']