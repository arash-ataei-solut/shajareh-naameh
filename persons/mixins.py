from django.contrib.auth.mixins import AccessMixin


class IsSubmitterMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_submitter:
            return super(IsSubmitterMixin, self).dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
