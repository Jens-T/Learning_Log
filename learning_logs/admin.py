from django.contrib import admin

from .models import Topic, Entry
from .models import Notification

admin.site.register(Notification)
admin.site.register(Topic)
admin.site.register(Entry)