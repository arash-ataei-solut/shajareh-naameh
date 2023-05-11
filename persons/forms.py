from django import forms

from persons.models import Person


class AddPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year',
            'birth_date', 'birth_place', 'residence_place',
            'death_year', 'death_date'
        ]
