from django.contrib import admin
from django.utils.translation import gettext as _

from persons.models import Person, RelationMatchingRequest


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'birth_year', 'matching_status')
    search_fields = ('first_name', 'last_name')
    list_filter = ('gender', 'matching_status')
    autocomplete_fields = ('father', 'mother', 'spouses')


@admin.register(RelationMatchingRequest)
class RelationMatchingRequestAdmin(admin.ModelAdmin):
    list_display = ('person', 'related_person', 'similar_related_person', 'relation', 'status')
    list_select_related = ('person', 'related_person', 'similar_related_person')
    list_filter = ('relation', 'status')
    search_fields = (
        'person__first_name',
        'person__last_name',
        'related_person__first_name',
        'related_person__last_name',
        'similar_related_person__first_name',
        'similar_related_person__last_name',
    )
    actions = ['undo_matching']

    @admin.action(permissions=['change'], description=_('لغو انطباق'))
    def undo_matching(self, request, queryset):
        for matching in queryset:
            matching.undo_the_matching()
