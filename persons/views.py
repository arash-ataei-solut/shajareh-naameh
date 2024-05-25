import copy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, UpdateView, DetailView
from django_htmx.http import HttpResponseClientRefresh, HttpResponseClientRedirect

from common.mixins import HTMXViewMixin, HTMXFormViewMixin
from persons import forms
from persons.forms import PersonAddForm, FindMyselfForm, PersonUpdateForm, PersonAddMyselfForm
from persons.mixins import IsSubmitterMixin
from persons.models import Person


class PersonAddView(LoginRequiredMixin, CreateView):
    template_name = 'persons/person_add.html'
    form_class = PersonAddForm
    success_url = reverse_lazy('persons:person-detail')


class PersonAddMyselfView(PersonAddView):
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


class PersonAddFatherView(HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_father.html'
    htmx_template_name = 'persons/htmx/person_add_father_htmx.html'
    form_class = forms.PersonAddFatherForm

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.person.pk})

    def get_person(self):
        self.person = get_object_or_404(Person, id=self.kwargs['person_id'])
        return self.person

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'person': self.get_person()})
        return kwargs


class PersonAddFatherMyselfView(PersonAddFatherView):
    def get_success_url(self):
        return reverse('persons:person-detail-myself')

    def get_person(self):
        if hasattr(self.request.user, 'person'):
            return self.request.user.person
        return Http404(
            "No Person matches the given query."
        )


class PersonAddMotherView(HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_mother.html'
    htmx_template_name = 'persons/htmx/person_add_mother_htmx.html'
    form_class = forms.PersonAddMotherForm

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.person.pk})

    def get_person(self):
        self.person = get_object_or_404(Person, id=self.kwargs['person_id'])
        return self.person

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'person': self.get_person()})
        return kwargs


class PersonAddMotherMyselfView(PersonAddMotherView):
    def get_success_url(self):
        return reverse('persons:person-detail-myself')

    def get_person(self):
        if hasattr(self.request.user, 'person'):
            return self.request.user.person
        return Http404(
            "No Person matches the given query."
        )


class PersonAddSpouseView(HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_spouse.html'
    htmx_template_name = 'persons/htmx/person_add_spouse_htmx.html'
    form_class = forms.PersonAddSpouseForm

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.person.pk})

    def get_person(self):
        self.person = get_object_or_404(Person, id=self.kwargs['person_id'])
        return self.person

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'person': self.get_person()})
        return kwargs


class PersonAddSpouseMyselfView(PersonAddSpouseView):
    def get_success_url(self):
        return reverse('persons:person-detail-myself')

    def get_person(self):
        if hasattr(self.request.user, 'person'):
            return self.request.user.person
        return Http404(
            "No Person matches the given query."
        )


class PersonAddChildView(HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_child.html'
    htmx_template_name = 'persons/htmx/person_add_child_htmx.html'
    form_class = forms.PersonAddChildForm

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.person.pk})

    def get_person(self):
        self.person = get_object_or_404(Person, id=self.kwargs['person_id'])
        return self.person

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'person': self.get_person()})
        return kwargs


class PersonAddChildMyselfView(PersonAddChildView):
    def get_success_url(self):
        return reverse('persons:person-detail-myself')

    def get_person(self):
        if hasattr(self.request.user, 'person'):
            return self.request.user.person
        return Http404(
            "No Person matches the given query."
        )


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
