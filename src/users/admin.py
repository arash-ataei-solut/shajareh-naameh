from django.contrib import admin

from users.models import ShnUser, Notification, AuthOTP


@admin.register(ShnUser)
class ShnUserAdmin(admin.ModelAdmin):
    pass


@admin.register(AuthOTP)
class AuthOtpAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'usage', 'confirmed')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'read')
    list_editable = ('read',)
