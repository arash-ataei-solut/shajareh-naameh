from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.utils.translation import gettext as _

from persons.models import Person


class IsPersonCreatedByOrIsOwner(LoginRequiredMixin):
    raise_exception = True
    permission_denied_message = _('شما دسترسی لازم، برای تغییر اطلاعات این شخص، را ندارید.')

    def get_object(self, queryset=None):
        obj: Person = super().get_object(queryset)
        if obj.created_by_id == self.request.user.id or obj.user_id == self.request.user.id:
            return obj
        return self.handle_no_permission()
