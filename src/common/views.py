from django.views.generic import TemplateView

from persons.models import Person
from users.models import ShnUser


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context.update(
            {
                'user_count': ShnUser.objects.all().count(),
                'person_count': Person.objects.all().count(),
            }
        )
        return context
