from django.views.generic import FormView

from common.htmx.forms import AnonymousTicketForm


class AnonymousTicketFormView(FormView):
    template_name = 'htmx/contact.html'
    form_class = AnonymousTicketForm
