from django.contrib import admin, messages
from django.utils.translation import gettext as _

from persons import models
from persons.exceptions import RelationMatchingRequestStatusPriorityError


@admin.register(models.SeeTreePermissionRequest)
class SeeTreePermissionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'person', 'applicant', 'status']
    search_fields = ['person__first_name', 'person__last_name', 'applicant__first_name', 'applicant__last_name']
    list_filter = ['status']
    actions = [
        'undo_see_tree_permission',
        'approve_see_tree_permission',
        'reject_see_tree_permission',
    ]
    
    @admin.action(permissions=['change'], description=_('لغو دسترسی مشاهده درخت‌خانوادگی'))
    def undo_see_tree_permission(self, request, queryset):
        for permission_request in queryset:
            permission_request.undo_permission_request()
    
    @admin.action(permissions=['change'], description=_('تایید دسترسی مشاهده درخت‌خانوادگی'))
    def approve_see_tree_permission(self, request, queryset):
        for permission_request in queryset:
            permission_request.approve_permission_request()
    
    @admin.action(permissions=['change'], description=_('رد دسترسی مشاهده درخت‌خانوادگی'))
    def reject_see_tree_permission(self, request, queryset):
        for permission_request in queryset:
            permission_request.reject_permission_request()


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'id', 'gender', 'birth_year', 'matching_status')
    search_fields = ('first_name', 'last_name', 'id', 'birth_year')
    list_filter = ('gender', 'matching_status')
    autocomplete_fields = ('father', 'mother', 'spouses')


@admin.register(models.RelationMatchingRequest)
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
