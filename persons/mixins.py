from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from persons.models import Person


class CanUpdateThePersonMixin:
    permission_denied_message = _('شما دسترسی لازم برای ویرایش یا مشاهده جزئیات اطلاعات این شخص را ندارید.')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            return self.handle_no_permission()

    def get_object(self, queryset=None):
        obj: Person = super().get_object(queryset)
        if obj.can_update(self.request.user):
            return obj
        raise PermissionDenied()


class CanDeleteThePersonMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            return self.handle_no_permission()

    def get_object(self, queryset=None):
        obj: Person = super().get_object(queryset)
        if obj.can_delete(self.request.user):
            return obj
        raise PermissionDenied()
