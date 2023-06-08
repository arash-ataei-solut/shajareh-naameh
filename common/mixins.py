class HTMXViewMixin:
    htmx_template_name = None

    def dispatch(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = self.htmx_template_name
        return super().dispatch(request, *args, **kwargs)
