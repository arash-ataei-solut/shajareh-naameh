from django.contrib import admin

from common.models import TicketCategory, AnonymousTicket


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(AnonymousTicket)
class AnonymousTicketAdmin(admin.ModelAdmin):
    pass
