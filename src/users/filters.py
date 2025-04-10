import django_filters
from django.utils.translation import gettext as _

from persons.models import Person


class PersonListFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains', label=_('اسم'))
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains', label=_('فامیلی'))
    father_first_name = django_filters.CharFilter(
        field_name='father__first_name', lookup_expr='icontains', label=_('اسم پدر')
    )
    mother_first_name = django_filters.CharFilter(
        field_name='mother__first_name', lookup_expr='icontains', label=_('اسم مادر')
    )
    class Meta:
        model = Person
        fields = {
            'gender': ['exact'],
            'birth_year': ['exact'],
        }
