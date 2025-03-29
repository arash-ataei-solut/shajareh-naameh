import django_filters

from persons.models import Person


class PersonListFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'gender': ['exact'],
            'birth_year': ['exact'],
        }
