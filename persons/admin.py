from django.contrib import admin, messages
from django.utils.translation import gettext as _

from persons.exceptions import RelationMatchingRequestStatusPriorityError
from persons.models import Person, RelationMatchingRequest


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'id', 'gender', 'birth_year', 'matching_status')
    search_fields = ('first_name', 'last_name', 'id', 'birth_year')
    list_filter = ('gender', 'matching_status')
    autocomplete_fields = ('father', 'mother', 'spouses')


@admin.register(RelationMatchingRequest)
class RelationMatchingRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'related_person', 'similar_related_person', 'relation', 'status')
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
    actions = ['do_matching_requests', 'undo_matching_requests', 'reject_matching_requests']

    @admin.action(permissions=['change'], description=_('انجام انطباق‌ها'))
    def do_matching_requests(self, request, queryset):
        with_status_error_matching_requests = []
        for matching in queryset:
            try:
                matching.do_the_matching()
            except RelationMatchingRequestStatusPriorityError:
                with_status_error_matching_requests.append(matching.id)
        if with_status_error_matching_requests:
            messages.error(
                request,
                _(
                    f'درخواست‌های ID:{with_status_error_matching_requests} در وضعیت اشتباه قرار دارند'
                    f' و امکان انحام انطباق آن‌ها وجود ندارد. برای انجام تطابق لازم است درخواست'
                    f' در وضعیت "در انتظار تایید تطابق" باشد.'
                )
            )

    @admin.action(permissions=['change'], description=_('لغو انطباق‌ها'))
    def undo_matching_requests(self, request, queryset):
        with_status_error_matching_requests = []
        for matching in queryset:
            try:
                matching.undo_the_matching()
            except RelationMatchingRequestStatusPriorityError:
                with_status_error_matching_requests.append(matching.id)
        if with_status_error_matching_requests:
            messages.error(
                request,
                _(
                    f'درخواست‌های ID:{with_status_error_matching_requests} در وضعیت اشتباه قرار دارند'
                    f' و امکان لغو انطباق آن‌ها وجود ندارد. برای لغو تطابق لازم است درخواست'
                    f' در یکی از وضعیت‌های "تطابق انجام شده" یا "تطابق رد شده" باشد.'
                )
            )

    @admin.action(permissions=['change'], description=_('رد انطباق‌ها'))
    def reject_matching_requests(self, request, queryset):
        with_status_error_matching_requests = []
        for matching in queryset:
            try:
                matching.reject_the_matching()
            except RelationMatchingRequestStatusPriorityError:
                with_status_error_matching_requests.append(matching.id)
        if with_status_error_matching_requests:
            messages.error(
                request,
                _(
                    f'درخواست‌های ID:{with_status_error_matching_requests} در وضعیت اشتباه قرار دارند'
                    f' و امکان رد انطباق آن‌ها وجود ندارد. برای رد تطابق لازم است درخواست'
                    f' در وضعیت "در انتظار تایید تطابق" باشد.'
                )
            )
