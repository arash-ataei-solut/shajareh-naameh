import copy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, UpdateView, DetailView

from common.mixins import HTMXViewMixin, HTMXFormViewMixin
from persons import forms
from persons.enums import MatchingStatusChoices, RelationRequestStatusChoices, RelationChoices
from persons.forms import PersonAddForm, FindMyselfForm, PersonUpdateForm, PersonAddMyselfForm
from persons.matchmakers import RelationMatchmaker
from persons.models import Person, RelationMatchingRequest


class PersonAddView(LoginRequiredMixin, CreateView):
    template_name = 'persons/person_add.html'
    form_class = PersonAddForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = copy.copy(kwargs['data'])
            data.update({'created_by': self.request.user})
            kwargs.update({'data': data})
        return kwargs

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.object.pk})


class PersonAddMyselfView(PersonAddView):
    template_name = 'persons/person_add_myself.html'
    form_class = PersonAddMyselfForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = kwargs['data']
            data.update({'user': self.request.user})
            kwargs.update({'data': data})
        return kwargs


class PersonUpdateView(HTMXFormViewMixin, UpdateView):
    template_name = 'persons/person_update.html'
    htmx_template_name = 'persons/htmx/person_update_htmx.html'
    form_class = PersonUpdateForm
    success_url = reverse_lazy('persons:person-detail')

    def get_queryset(self):
        return Person.objects.filter(Q(user=self.request.user) | Q(created_by=self.request.user))

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.object.pk})


class PersonAddRelativeMixin:
    relation: RelationChoices = None

    def get(self, request, *args, **kwargs):
        self.person = self.get_person()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.person = self.get_person()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return reverse('persons:person-detail', kwargs={'pk': self.person.pk})

    def get_person(self):
        queryset = Person.objects.filter(Q(user=self.request.user) | Q(created_by=self.request.user))
        return get_object_or_404(queryset, id=self.kwargs['person_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'person': self.person})
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'person': self.person})
        return kwargs

    def form_valid(self, form):
        related_person = form.save()
        matchmaker = RelationMatchmaker(related_person, self.person, self.relation)
        if matchmaker.match_exists():
            matching_request = matchmaker.create_matching_request()
            success_url = reverse('persons:relation-request-select-similar', kwargs={'pk': matching_request.pk})
            return HttpResponseRedirect(success_url)
        return self.success_response()


class PersonAddFatherView(PersonAddRelativeMixin, HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_father.html'
    htmx_template_name = 'persons/htmx/person_add_father_htmx.html'
    form_class = forms.PersonAddFatherForm
    relation = RelationChoices.FATHER
    # TODO Handle loop


class PersonAddMotherView(PersonAddRelativeMixin, HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_mother.html'
    htmx_template_name = 'persons/htmx/person_add_mother_htmx.html'
    form_class = forms.PersonAddMotherForm
    relation = RelationChoices.MOTHER


class PersonAddSpouseView(PersonAddRelativeMixin, HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_spouse.html'
    htmx_template_name = 'persons/htmx/person_add_spouse_htmx.html'
    form_class = forms.PersonAddSpouseForm
    relation = RelationChoices.SPOUSE


class PersonAddChildView(PersonAddRelativeMixin, HTMXFormViewMixin, PersonAddView):
    template_name = 'persons/person_add_child.html'
    htmx_template_name = 'persons/htmx/person_add_child_htmx.html'
    form_class = forms.PersonAddChildForm
    relation = RelationChoices.CHILD


class PersonDetailView(LoginRequiredMixin, DetailView):
    template_name = 'persons/person_detail.html'

    def get_queryset(self):
        return Person.objects.filter(
            Q(matching_status=MatchingStatusChoices.NO_MATCH) &
            (Q(user=self.request.user) | Q(created_by=self.request.user))

        )


class PersonTreeView(HTMXViewMixin, PersonDetailView):
    template_name = 'persons/person_tree.html'
    htmx_template_name = 'persons/htmx/person-tree-htmx.html'


class RelationRequestSelectSimilarView(HTMXFormViewMixin, LoginRequiredMixin, UpdateView):
    template_name = 'persons/relation_request_set_similar.html'
    htmx_template_name = 'persons/htmx/relation_request_set_similar_htmx.html'
    form_class = forms.RelationRequestSetSimilarForm

    def get_queryset(self):
        return RelationMatchingRequest.objects.filter(status=RelationRequestStatusChoices.AWAITING_SIMILAR)

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.object.person.pk})


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
