from django import forms
from django.utils.translation import gettext as _

from persons.models import Person


class FindMyselfForm(forms.Form):
    first_name = forms.CharField(label=_('نام'))
    last_name = forms.CharField(label=_('نام حانوادگی'))
    father_name = forms.CharField(label=_('نام پدر'))
    mother_name = forms.CharField(label=_('نام مادر'))

    def find_me(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        father_name = self.cleaned_data['father_name']
        mother_name = self.cleaned_data['mother_name']
        my_person_qs = Person.objects.find_me(first_name, last_name, father_name, mother_name)
        return my_person_qs
