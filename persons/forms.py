from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.htmx.forms import PlaceholderFormMixin
from persons import enums
from persons.models import Person
from places.forms import PlaceWidget


class PersonAddForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year',
        ]
        widgets = {
            'birth_place': PlaceWidget
        }


class PersonAddMyselfForm(PlaceholderFormMixin, forms.ModelForm):
    user = forms.HiddenInput()

    class Meta:
        model = Person
        fields = [
            'user', 'first_name', 'last_name', 'gender', 'birth_year',
        ]


class PersonAddFatherForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'birth_year'
        ]

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.person.father:
            raise ValidationError(
                'پدر این شخص ثبت شده‌است.', code='duplicate_mother'
            )

    def save(self, commit=True):
        self.instance.gender = enums.GenderChoices.MALE
        father = super().save(commit)
        self.person.father = father
        self.person.save()
        return father


class PersonAddMotherForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'birth_year'
        ]

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.person.mother:
            raise ValidationError(
                'مادر این شخص ثبت شده‌است.', code='duplicate_mother'
            )

    def save(self, commit=True):
        self.instance.gender = enums.GenderChoices.FEMALE
        mother = super().save(commit)
        self.person.mother = mother
        self.person.save()
        return mother


class PersonUpdateForm(PlaceholderFormMixin, forms.ModelForm):
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
