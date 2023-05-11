from django.views.generic import CreateView

from persons.forms import AddPersonForm


class AddPersonView(CreateView):
    template_name = 'add_person.html'
    form_class = AddPersonForm
