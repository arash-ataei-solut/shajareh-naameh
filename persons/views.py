import copy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, DetailView

from common.mixins import HTMXViewMixin
from persons.forms import PersonAddForm, FindMyselfForm, PersonUpdateForm, PersonAddMyselfForm
from persons.mixins import IsSubmitterMixin
from persons.models import Person


class PersonAddView(LoginRequiredMixin, IsSubmitterMixin, CreateView):
    template_name = 'persons/person_add.html'
    form_class = PersonAddForm
    success_url = reverse_lazy('persons:person-detail')


class PersonAddMyselfView(LoginRequiredMixin, IsSubmitterMixin, CreateView):
    template_name = 'persons/person_add_myself.html'
    form_class = PersonAddMyselfForm
    success_url = reverse_lazy('persons:person-detail-myself')

    def get_form_kwargs(self):
        kwargs = super(PersonAddMyselfView, self).get_form_kwargs()
        if self.request.method == 'POST':
            data = copy.copy(kwargs['data'])
            data.update({'user': self.request.user})
            kwargs.update({'data': data})
        return kwargs


class PersonUpdateView(LoginRequiredMixin, IsSubmitterMixin, UpdateView):
    template_name = 'persons/person_update.html'
    form_class = PersonUpdateForm
    queryset = Person.objects.all()
    success_url = reverse_lazy('persons:person-detail')


class PersonDetailView(LoginRequiredMixin, IsSubmitterMixin, DetailView):
    template_name = 'persons/person_detail.html'
    queryset = Person.objects.all()


class PersonDetailMyselfView(LoginRequiredMixin, IsSubmitterMixin, DetailView):
    template_name = 'persons/person_detail_myself.html'
    queryset = Person.objects.all()

    def get_object(self, queryset=None):
        return get_object_or_404(Person, user_id=self.request.user.id)


class FindMyselfView(HTMXViewMixin, LoginRequiredMixin, FormView):
    form_class = FindMyselfForm
    template_name = 'persons/find_myself.html'
    htmx_template_name = 'persons/htmx/find_myself_htmx.html'

    def form_valid(self, form):
        myself_person_queryset = form.find_myself_queryset()
        context = self.get_context_data()
        context.update(
            {
                'myself_person_list': myself_person_queryset,
                'myself_person_exists': myself_person_queryset.exists(),
            }
        )
        if self.request.htmx:
            list_template_name = 'persons/htmx/find_myself_list_htmx.html'
        else:
            list_template_name = 'persons/find_myself_list.html'

        return TemplateResponse(
            request=self.request,
            template=list_template_name,
            context=context,
        )
