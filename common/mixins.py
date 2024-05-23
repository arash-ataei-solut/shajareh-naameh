from django.http import HttpResponseRedirect
from django_htmx.http import HttpResponseClientRedirect


class HTMXViewMixin:
    htmx_template_name = None

    def dispatch(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = self.htmx_template_name
        return super().dispatch(request, *args, **kwargs)


class HTMXFormViewMixin(HTMXViewMixin):
    def success_response(self):
        if self.request.htmx:
            return HttpResponseClientRedirect(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        super().form_valid(form)
        return self.success_response()
