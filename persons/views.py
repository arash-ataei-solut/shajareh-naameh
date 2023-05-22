from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from persons.forms import AddPersonForm
from persons.mixins import IsSubmitterMixin


class AddPersonView(LoginRequiredMixin, IsSubmitterMixin, CreateView):
    template_name = 'add_person.html'
    form_class = AddPersonForm
