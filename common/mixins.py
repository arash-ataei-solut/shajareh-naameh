from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_htmx.http import HttpResponseClientRedirect, HttpResponseClientRefresh


class OnlyHTMXViewMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.htmx:
            return super().dispatch(request, *args, **kwargs)
        return Http404()

    def http_redirect(self, url):
        return HttpResponseClientRedirect(url)


class HTMXViewMixin:
    htmx_template_name = None

    def http_redirect(self, url):
        if self.request.htmx:
            return HttpResponseClientRedirect(url)
        return HttpResponseRedirect(url)

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = self.htmx_template_name
        return super().dispatch(request, *args, **kwargs)


class HTMXFormViewMixin(HTMXViewMixin):
    def success_response(self):
        return self.http_redirect(self.get_success_url())

    def form_valid(self, form):
        super().form_valid(form)
        return self.success_response()


class OnlyHTMXFormViewMixin(OnlyHTMXViewMixin):
    def success_response(self):
        return HttpResponseClientRefresh()

    def form_valid(self, form):
        super().form_valid(form)
        return self.success_response()
