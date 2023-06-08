from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView

from persons.htmx.forms import FindMyselfForm, AddMyPersonForm
from persons.models import Person


class FindMyselfView(LoginRequiredMixin, FormView):
    form_class = FindMyselfForm
    template_name = 'profile/htmx/find_myself_htmx.html'

    def form_valid(self, form):
        my_person_qs = form.find_me()
        if my_person_qs:
            return super(FindMyselfView, self).form_valid(form)
        return super(FindMyselfView, self).form_valid(form)


class AddMyPersonView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = AddMyPersonForm

    def get_form_kwargs(self):
        kwargs = super(AddMyPersonView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
