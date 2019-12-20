from django.contrib import admin
from .models import Resolution, Comment, Entry, Photo

# Register your models here.
admin.site.register(Resolution)
admin.site.register(Comment)
admin.site.register(Entry)
admin.site.register(Photo)
