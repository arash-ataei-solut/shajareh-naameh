from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django_htmx.http import HttpResponseClientRedirect, HttpResponseClientRefresh


class OnlyHTMXViewMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.htmx:
            return super().dispatch(request, *args, **kwargs)
        raise Http404()

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


class AtomicViewMixin:
    @transaction.atomic
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TemplatePermissionDeniedErrorHTMXViewMixin:
    def handle_no_permission(self):
        if self.request.htmx:
            template = 'htmx/permission_denied_htmx.html'
        else:
            template = 'permission_denied.html'
        context = {
            'permission_denied_message': self.get_permission_denied_message()
        }
        return TemplateResponse(
            request=self.request,
            template=template,
            context=context,
        )
