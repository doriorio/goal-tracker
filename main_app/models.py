from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


MOODS = (
    ('H', 'Happy'),
    ('M', 'Meh'),
    ('S', 'Sad')
)

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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField('comment', max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_at']

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE)
    mood = models.CharField(
        max_length=1,
        choices=MOODS,
        default=MOODS[1][0],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.CharField(max_length=15)
    notes = models.CharField(max_length=150)
    Sun = models.BooleanField(default=False)
    Mon = models.BooleanField(default=False)
    Tue = models.BooleanField(default=False)
    Wed = models.BooleanField(default=False)
    Thu = models.BooleanField(default=False)
    Fri = models.BooleanField(default=False)
    Sat = models.BooleanField(default=False)
    def __str__(self):
        return self.week
    def get_absolute_url(self):
        return reverse('entry_index', kwargs={ 'resolution_id': self.resolution_id })

class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for user: {self.user.username} @{self.url}'