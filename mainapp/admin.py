from django.contrib import admin

# Register your models here.
from .models import event,eventtoken
admin.site.register(event)
admin.site.register(eventtoken)