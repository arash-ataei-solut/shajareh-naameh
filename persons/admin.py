from django.contrib import admin

from persons.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'birth_year')
    search_fields = ('first_name', 'last_name')
    autocomplete_fields = ('father', 'mother', 'spouses')


admin.site.register(Person, PersonAdmin)
