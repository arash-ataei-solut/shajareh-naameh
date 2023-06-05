from django.contrib import admin

from users.models import ShnUser, Notification


@admin.register(ShnUser)
class ShnUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'read')
    list_editable = ('read',)
