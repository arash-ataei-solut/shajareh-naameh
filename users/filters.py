import django_filters

from persons.models import Person


class PersonListFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'gender',
            'birth_year',
        ]
