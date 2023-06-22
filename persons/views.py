from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.views.generic import CreateView, FormView

from common.mixins import HTMXViewMixin
from persons.forms import AddPersonForm, FindMyselfForm
from persons.mixins import IsSubmitterMixin


class AddPersonView(LoginRequiredMixin, IsSubmitterMixin, CreateView):
    template_name = 'persons/add_person.html'
    form_class = AddPersonForm


class FindMyselfView(HTMXViewMixin, LoginRequiredMixin, FormView):
    form_class = FindMyselfForm
    template_name = 'persons/find_myself.html'
    htmx_template_name = 'persons/htmx/find_myself_htmx.html'

    def form_valid(self, form):
        myself_person_queryset = form.find_myself_queryset()
        context = self.get_context_data()
        context.update(
            {
                'myself_person_queryset': myself_person_queryset,
                'myself_person_does_not_exist': not myself_person_queryset.exists(),
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
            using=self.template_engine,
        )
