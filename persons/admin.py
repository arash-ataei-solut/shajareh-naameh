from django.contrib import admin

from persons.models import Person


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('father', 'mother', 'spouse', )
    autocomplete_fields = ('father', 'mother', 'spouse', )


admin.site.register(Person, PersonAdmin)
