from django import forms
from django.utils.translation import gettext as _

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


class FindMyselfForm(forms.Form):
    first_name = forms.CharField(label=_('نام'))
    last_name = forms.CharField(label=_('نام خانوادگی'))
    father_name = forms.CharField(label=_('نام پدر'))
    mother_name = forms.CharField(label=_('نام مادر'))

    def find_myself_queryset(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        father_name = self.cleaned_data['father_name']
        mother_name = self.cleaned_data['mother_name']
        my_person_qs = Person.objects.find_myself(first_name, last_name, father_name, mother_name)
        return my_person_qs
