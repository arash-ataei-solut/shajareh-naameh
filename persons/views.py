from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView

from persons.forms import AddPersonForm, FindMyselfForm
from persons.mixins import IsSubmitterMixin


class AddPersonView(LoginRequiredMixin, IsSubmitterMixin, CreateView):
    template_name = 'persons/add_person.html'
    form_class = AddPersonForm


class FindMyselfView(LoginRequiredMixin, FormView):
    form_class = FindMyselfForm
    template_name = 'persons/find_myself.html'
