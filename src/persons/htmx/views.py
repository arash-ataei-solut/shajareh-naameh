from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView

from persons.forms import FindMyselfForm
from persons.htmx.forms import AddMyPersonForm
from persons.models import Person


class AddMyPersonView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = AddMyPersonForm

    def get_form_kwargs(self):
        kwargs = super(AddMyPersonView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
