from django.contrib import admin

from persons.models import Person, RelationMatchingRequest


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'birth_year', 'matching_status')
    search_fields = ('first_name', 'last_name')
    list_filter = ('gender', 'matching_status')
    autocomplete_fields = ('father', 'mother', 'spouses')


@admin.register(RelationMatchingRequest)
class RelationMatchingRequestAdmin(admin.ModelAdmin):
    list_display = ('person', 'related_person', 'similar_related_person', 'relation')
    list_select_related = ('person', 'related_person', 'similar_related_person')
    list_filter = ('relation',)
    search_fields = (
        'person__first_name',
        'person__last_name',
        'related_person__first_name',
        'related_person__last_name',
        'similar_related_person__first_name',
        'similar_related_person__last_name',
    )


admin.site.register(Person, PersonAdmin)
