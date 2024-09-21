import copy

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, DetailView, TemplateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django_htmx.http import HttpResponseClientRefresh

from common.mixins import HTMXViewMixin, OnlyHTMXViewMixin, OnlyHTMXFormViewMixin, \
    HTMXModelFormViewMixin, OnlyHTMXModelFormViewMixin, AtomicViewMixin, TemplatePermissionDeniedErrorHTMXViewMixin
from persons import forms
from persons.enums import RelationMatchingRequestStatusChoices, RelationChoices
from persons.exceptions import RelationMatchingRequestStatusPriorityError
from persons.forms import PersonAddForm, FindMyselfForm, PersonUpdateForm, PersonAddMyselfForm
from persons.matchmakers import RelationMatchmaker
from persons.mixins import CanUpdateThePersonMixin, CanDeleteThePersonMixin
from persons.models import Person, RelationMatchingRequest
from places.models import ResidencePlace


class PersonAddViewMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = copy.copy(kwargs['data'])
            data.update({'created_by': self.request.user})
            kwargs.update({'data': data})
        return kwargs

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.object.pk})
    
    
class PersonAddView(AtomicViewMixin, LoginRequiredMixin, PersonAddViewMixin, CreateView):
    template_name = 'persons/person_add.html'
    form_class = PersonAddForm


class PersonAddMyselfViewMixin(AtomicViewMixin, LoginRequiredMixin, PersonAddViewMixin, CreateView):
    template_name = 'persons/person_add_myself.html'
    form_class = PersonAddMyselfForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = kwargs['data']
            data.update({'user': self.request.user, 'created_by': self.request.user})
            kwargs.update({'data': data})
        return kwargs


class PersonAddResidencePlaceView(LoginRequiredMixin, OnlyHTMXModelFormViewMixin, CreateView):
    template_name = 'persons/htmx/person_add_residence_place_htmx.html'
    form_class = forms.PersonAddResidenceForm

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
        queryset = Person.objects.exclude_matched_persons().filter(Q(user=self.request.user) | Q(created_by=self.request.user))
        return get_object_or_404(queryset, id=self.kwargs['person_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'person': self.person})
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'person': self.person})
        return kwargs


class PersonUpdateResidencePlaceView(LoginRequiredMixin, OnlyHTMXModelFormViewMixin, UpdateView):
    template_name = 'persons/htmx/person_update_residence_place_htmx.html'
    form_class = forms.PersonUpdateResidencePlaceForm

    def get_queryset(self):
        return ResidencePlace.objects.filter(
            Q(person__user=self.request.user) | Q(person__created_by=self.request.user)
        )


class PersonDeleteResidencePlaceConfirmationView(LoginRequiredMixin, OnlyHTMXViewMixin, DetailView):
    template_name = 'persons/htmx/person_delete_residence_place_confirmation_htmx.html'

    def get_queryset(self):
        return ResidencePlace.objects.filter(
            Q(person__user=self.request.user) | Q(person__created_by=self.request.user)
        )


class PersonDeleteResidencePlaceView(LoginRequiredMixin, OnlyHTMXFormViewMixin, DeleteView):
    def get_queryset(self):
        return ResidencePlace.objects.filter(
            Q(person__user=self.request.user) | Q(person__created_by=self.request.user)
        )

    def form_valid(self, form):
        place = str(self.object.place)
        self.object.delete()
        messages.success(
            self.request,
            _(f'محل سکونت مورد نظر با نام محله/روستا "{place}" با موفقیت حذف شد.')
        )
        return super().form_valid(form)


class PersonAddRelativeMixin(OnlyHTMXFormViewMixin):
    relation: RelationChoices = None
    raise_exception = True
    permission_denied_message = _('شما دسترسی لازم برای ویرایش یا مشاهده جزئیات اطلاعات این شخص را ندارید.')

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
        queryset = Person.objects.exclude_matched_persons()
        obj = get_object_or_404(queryset, id=self.kwargs['person_pk'])
        if obj.can_update(self.request.user):
            return obj
        return self.handle_no_permission()

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
            matching_request = matchmaker.create_matching_request(self.request.user)
            success_url = reverse('persons:relation-matching-request-select-similar', kwargs={'pk': matching_request.pk})
            return HttpResponseRedirect(success_url)
        return super().form_valid(form)


class PersonAddFatherViewMixin(AtomicViewMixin, LoginRequiredMixin, PersonAddRelativeMixin, PersonAddViewMixin, CreateView):
    template_name = 'persons/htmx/person_add_father_htmx.html'
    form_class = forms.PersonAddFatherForm
    relation = RelationChoices.FATHER
    # TODO Handle loop


class PersonAddMotherViewMixin(AtomicViewMixin, LoginRequiredMixin, PersonAddRelativeMixin, PersonAddViewMixin, CreateView):
    template_name = 'persons/htmx/person_add_mother_htmx.html'
    form_class = forms.PersonAddMotherForm
    relation = RelationChoices.MOTHER


class PersonAddSpouseViewMixin(AtomicViewMixin, LoginRequiredMixin, PersonAddRelativeMixin, PersonAddViewMixin, CreateView):
    template_name = 'persons/htmx/person_add_spouse_htmx.html'
    form_class = forms.PersonAddSpouseForm
    relation = RelationChoices.SPOUSE


class PersonAddChildViewMixin(AtomicViewMixin, LoginRequiredMixin, PersonAddRelativeMixin, PersonAddViewMixin, CreateView):
    template_name = 'persons/htmx/person_add_child_htmx.html'
    form_class = forms.PersonAddChildForm
    relation = RelationChoices.CHILD


# Person delete relatives

class PersonDeleteAncestorConfirmationView(
    TemplatePermissionDeniedErrorHTMXViewMixin,
    LoginRequiredMixin,
    CanDeleteThePersonMixin,
    OnlyHTMXViewMixin,
    DetailView,
):
    template_name = 'persons/htmx/person_delete_ancestor_confirmation_htmx.html'
    queryset = Person.objects.exclude_matched_persons()
    permission_denied_message = _('شما دسترسی لازم برای حذف این شخص را ندارید.')


class PersonDeleteAncestorView(LoginRequiredMixin, CanDeleteThePersonMixin, OnlyHTMXFormViewMixin, DeleteView):
    queryset = Person.objects.exclude_matched_persons()

    def get_failure_url(self):
        return reverse('persons:person-delete-ancestor-failure', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        failure_conditions: list[bool] = [
            self.object.father_id is not None,
            self.object.mother_id is not None,
            self.object.father_children.count() + self.object.mother_children.count() > 1,
        ]

        if any(failure_conditions):
            return HttpResponseRedirect(self.get_failure_url())

        full_name = self.object.full_name
        self.object.delete()
        messages.success(
            self.request,
            _(f'شخص مورد نظر با نام "{full_name}" با موفقیت حذف شد.')
        )
        return super().form_valid(form)


class PersonDeleteAncestorFailureView(LoginRequiredMixin, OnlyHTMXViewMixin, DetailView):
    template_name = 'persons/htmx/person_delete_ancestor_failure_htmx.html'

    def get_queryset(self):
        return Person.objects.exclude_matched_persons().filter(created_by=self.request.user)


class PersonDeleteDescendantConfirmationView(
    TemplatePermissionDeniedErrorHTMXViewMixin,
    LoginRequiredMixin,
    CanDeleteThePersonMixin,
    OnlyHTMXViewMixin,
    DetailView,
):
    template_name = 'persons/htmx/person_delete_descendant_confirmation_htmx.html'
    queryset = Person.objects.exclude_matched_persons()
    permission_denied_message = _('شما دسترسی لازم برای حذف این شخص را ندارید.')


class PersonDeleteDescendantView(LoginRequiredMixin, OnlyHTMXFormViewMixin, DeleteView):
    queryset = Person.objects.exclude_matched_persons()

    def form_valid(self, form):
        failure_conditions: list[bool] = [
            self.object.father_id is not None and self.object.mother_id is not None,
            self.object.father_children.count() > 0,
            self.object.mother_children.count() > 0,
        ]
        if any(failure_conditions):
            return HttpResponseRedirect(self.get_failure_url())
        full_name = self.object.full_name
        self.object.delete()
        messages.success(
            self.request,
            _(f'شخص مورد نظر با نام "{full_name}" با موفقیت حذف شد.')
        )
        return super().form_valid(form)


class PersonDeleteDescendantFailureView(LoginRequiredMixin, OnlyHTMXViewMixin, DetailView):
    template_name = 'persons/htmx/person_delete_descendant_failure_htmx.html'

    def get_queryset(self):
        return Person.objects.exclude_matched_persons().filter(created_by=self.request.user)


class PersonDeleteSpouseConfirmationView(
    TemplatePermissionDeniedErrorHTMXViewMixin,
    LoginRequiredMixin,
    CanDeleteThePersonMixin,
    OnlyHTMXViewMixin,
    DetailView
):
    template_name = 'persons/htmx/person_delete_spouse_confirmation_htmx.html'
    queryset = Person.objects.exclude_matched_persons()
    permission_denied_message = _('شما دسترسی لازم برای حذف این شخص را ندارید.')


class PersonDeleteSpouseView(LoginRequiredMixin, CanDeleteThePersonMixin, OnlyHTMXFormViewMixin, DeleteView):
    queryset = Person.objects.exclude_matched_persons()

    def get_failure_url(self):
        return reverse('persons:person-delete-spouse-failure', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        failure_conditions: list[bool] = [
            self.object.father_id is not None,
            self.object.mother_id is not None,
            self.object.father_children.count() > 0,
            self.object.mother_children.count() > 0,
        ]
        if any(failure_conditions):
            return HttpResponseRedirect(self.get_failure_url())
        full_name = self.object.full_name
        self.object.delete()
        messages.success(
            self.request,
            _(f'شخص مورد نظر با نام "{full_name}" با موفقیت حذف شد.')
        )
        return super().form_valid(form)


class PersonDeleteSpouseFailureView(LoginRequiredMixin, OnlyHTMXViewMixin, DetailView):
    template_name = 'persons/htmx/person_delete_spouse_failure_htmx.html'

    def get_queryset(self):
        return Person.objects.exclude_matched_persons().filter(created_by=self.request.user)


# Person delete

class PersonDeleteConfirmationView(
    TemplatePermissionDeniedErrorHTMXViewMixin,
    LoginRequiredMixin,
    CanDeleteThePersonMixin,
    OnlyHTMXViewMixin,
    DetailView
):
    template_name = 'persons/htmx/person_delete_confirmation_htmx.html'
    queryset = Person.objects.exclude_matched_persons()
    permission_denied_message = _('شما دسترسی لازم برای حذف این شخص را ندارید.')


class PersonDeleteView(LoginRequiredMixin, CanDeleteThePersonMixin, OnlyHTMXFormViewMixin, DeleteView):
    queryset = Person.objects.exclude_matched_persons()

    def get_failure_url(self):
        return reverse('persons:person-delete-failure', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        failure_conditions: list[bool] = [
            self.object.father_id is not None,
            self.object.mother_id is not None,
            self.object.father_children.count() > 0,
            self.object.mother_children.count() > 0,
        ]
        if any(failure_conditions):
            return HttpResponseRedirect(self.get_failure_url())
        full_name = self.object.full_name
        self.object.delete()
        messages.success(
            self.request,
            _(f'شخص مورد نظر با نام "{full_name}" با موفقیت حذف شد.')
        )
        return super().form_valid(form)


class PersonDeleteFailureView(LoginRequiredMixin, OnlyHTMXViewMixin, DetailView):
    template_name = 'persons/htmx/person_delete_failure_htmx.html'

    def get_queryset(self):
        return Person.objects.exclude_matched_persons().filter(created_by=self.request.user)


class PersonDetailView(LoginRequiredMixin, CanUpdateThePersonMixin, DetailView):
    template_name = 'persons/person_detail.html'
    model = Person
    queryset = Person.objects.exclude_matched_persons()


class PersonUpdateView(LoginRequiredMixin, CanUpdateThePersonMixin, OnlyHTMXModelFormViewMixin, UpdateView):
    template_name = 'persons/htmx/person_update_htmx.html'
    form_class = PersonUpdateForm
    queryset = Person.objects.exclude_matched_persons()


# Person tree

class SeeTreePermissionRequestCreateView(LoginRequiredMixin, HTMXModelFormViewMixin, CreateView):
    template_name = 'persons/see_tree_permission_request_create.html'
    htmx_template_name = 'persons/htmx/person_see_tree_permission_request_htmx.html'
    form_class = forms.SeeTreePermissionRequestCreateForm

    def get(self, request, *args, **kwargs):
        self.person = self.get_person()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.person = self.get_person()
        return super().post(request, *args, **kwargs)

    def get_person(self):
        return get_object_or_404(Person, id=self.kwargs['person_pk'])

    def get_success_url(self):
        url = reverse('persons:see-tree-permission-request-success')
        previous_person_pk = self.request.GET.get('previous_person_pk') or ''
        return f'{url}?previous_person_pk={previous_person_pk}'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = copy.copy(kwargs['data'])
            data.update(
                {
                    'person': self.person,
                    'applicant': self.request.user,
                }
            )
            kwargs.update({'data': data})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'person': self.person,
                'previous_person_pk': self.request.GET.get('previous_person_pk')
            }
        )
        return context


class SeeTreePermissionRequestSuccessView(TemplateView):
    template_name = 'persons/see_tree_permission_request_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'previous_person_pk': self.request.GET.get('previous_person_pk')
            }
        )
        return context


class PersonTreeView(LoginRequiredMixin, HTMXViewMixin, DetailView):
    template_name = 'persons/person_tree.html'
    htmx_template_name = 'persons/htmx/person_tree_htmx.html'
    queryset = Person.objects.exclude_matched_persons()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.object.can_see_tree(request.user):
            return response

        if self.object.has_awaiting_see_tree_request(request.user):
            url = reverse('persons:see-tree-permission-request-success')
            previous_person_pk = self.request.GET.get('previous_person_pk') or ''
            return self.htmx_http_redirect(f'{url}?previous_person_pk={previous_person_pk}')

        url = reverse(
            'persons:see-tree-permission-request-create',
            kwargs={'person_pk': self.object.pk},
        )
        previous_person_pk = self.request.GET.get('previous_person_pk') or ''
        return self.htmx_http_redirect(f'{url}?previous_person_pk={previous_person_pk}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'has_awaiting_see_tree_permission_request': self.object.can_see_tree(self.request.user)
            }
        )
        return context


class PersonActionsInTreeView(LoginRequiredMixin, OnlyHTMXViewMixin, DetailView):
    template_name = 'persons/htmx/person_actions_in_tree_htmx.html'
    queryset = Person.objects.exclude_matched_persons()

    def get_context_data(self, **kwargs):
        context = super(PersonActionsInTreeView, self).get_context_data(**kwargs)
        context.update(
            {
                'can_update': self.object.can_update(self.request.user),
            }
        )
        return context


# Relation request

class RelationMatchingRequestSelectSimilarView(LoginRequiredMixin, OnlyHTMXModelFormViewMixin, UpdateView):
    template_name = 'persons/htmx/relation_matching_request_set_similar_htmx.html'
    form_class = forms.RelationMatchingRequestSetSimilarForm

    def get_queryset(self):
        return RelationMatchingRequest.objects.filter(
            related_person__created_by=self.request.user,
            status=RelationMatchingRequestStatusChoices.AWAITING_SIMILAR
        )

    def get_success_url(self):
        return reverse('persons:person-detail', kwargs={'pk': self.object.person.pk})


class RelationMatchingRequestRemoveSimilarView(LoginRequiredMixin, OnlyHTMXViewMixin, SingleObjectMixin, View):
    def get_queryset(self):
        return RelationMatchingRequest.objects.filter(related_person__created_by_id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        self.object: RelationMatchingRequest = self.get_object()
        try:
            self.object.remove_similar()
            messages.success(
                request,
                _('درخواست تطابق مورد نظر با موفقیت لغو شد.')
            )
            return HttpResponseClientRefresh()
        except RelationMatchingRequestStatusPriorityError:
            messages.error(
                request,
                _('امکان لغو درخواست تطابق مورد نظر وجود ندارد.'),
                extra_tags='danger'
            )
            return HttpResponseClientRefresh()


class RelationMatchingRequestConfirmationView(LoginRequiredMixin, OnlyHTMXModelFormViewMixin, UpdateView):
    template_name = 'persons/htmx/relation_matching_request_confirmation_htmx.html'
    form_class = forms.RelationMatchingRequestConfirmationForm

    def get_queryset(self):
        return RelationMatchingRequest.objects.filter(similar_related_person__created_by=self.request.user)
    
    def form_invalid(self, form):
        return super(RelationMatchingRequestConfirmationView, self).form_invalid(form)
    
    def form_valid(self, form):
        return super(RelationMatchingRequestConfirmationView, self).form_valid(form)



class FindMyselfView(LoginRequiredMixin, HTMXViewMixin, FormView):
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
