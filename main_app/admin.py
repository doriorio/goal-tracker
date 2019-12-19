from django.contrib import admin
from .models import Resolution
from .models import Comment

# Register your models here.
admin.site.register(Resolution)
admin.site.register(Comment)
