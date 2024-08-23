from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_htmx.http import HttpResponseClientRedirect, HttpResponseClientRefresh


class OnlyHTMXViewMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.htmx:
            return super().dispatch(request, *args, **kwargs)
        return Http404()

    def htmx_http_redirect(self, url):
        return HttpResponseClientRedirect(url)


class HTMXViewMixin:
    htmx_template_name = None

    def htmx_http_redirect(self, url):
        if self.request.htmx:
            return HttpResponseClientRedirect(url)
        return HttpResponseRedirect(url)

    def get_template_names(self):
        if self.request.htmx:
            if self.htmx_template_name is None:
                raise ImproperlyConfigured(
                    "TemplateResponseMixin requires either a definition of "
                    "'htmx_template_name' or an implementation of 'get_template_names()'"
                )
            return [self.htmx_template_name]
        else:
            return super().get_template_names()

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class HTMXFormViewMixin(HTMXViewMixin):
    def form_valid(self, form):
        return self.htmx_http_redirect(self.get_success_url())


class HTMXModelFormViewMixin(HTMXFormViewMixin):
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class OnlyHTMXFormViewMixin(OnlyHTMXViewMixin):
    def form_valid(self, form):
        return HttpResponseClientRefresh()


class OnlyHTMXModelFormViewMixin(OnlyHTMXFormViewMixin):
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
