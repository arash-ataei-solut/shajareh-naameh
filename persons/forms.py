from django import forms
from django.contrib.admin.widgets import AutocompleteSelect

from common.htmx.forms import PlaceholderFormMixin
from persons.models import Person
from places.forms import PlaceWidget


class AddPersonForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year',
            'birth_date', 'birth_place', 'residence_place',
            'death_year', 'death_date'
        ]
        widgets = {
            'birth_place': PlaceWidget
        }
