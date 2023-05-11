from django.contrib import admin

from users.models import ShnUser, Notification

admin.site.register(ShnUser)
admin.site.register(Notification)
