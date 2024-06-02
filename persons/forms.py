from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django_jalali.forms import jDateField, jDateInput

from common.htmx.forms import PlaceholderFormMixin
from persons import enums
from persons.models import Person
from places.forms import PlaceWidget


class PersonAddForm(PlaceholderFormMixin, forms.ModelForm):
    created_by = forms.HiddenInput()

    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]


class PersonAddMyselfForm(PlaceholderFormMixin, forms.ModelForm):
    user = forms.HiddenInput()
    created_by = forms.HiddenInput()

    class Meta:
        model = Person
        fields = [
            'user', 'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]


class PersonUpdateForm(PlaceholderFormMixin, forms.ModelForm):
    birth_date = jDateField(input_formats=['%Y/%m/%d'])

    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year',
            'birth_date', 'birth_place', 'death_year', 'death_date'
        ]
        widgets = {
            'birth_place': PlaceWidget,
        }


class PersonAddFatherForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.person.father:
            raise ValidationError(
                'پدر این شخص ثبت شده‌است.', code='duplicate_mother'
            )
        return super().clean()

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
            'first_name', 'last_name', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.person.mother:
            raise ValidationError(
                'مادر این شخص ثبت شده‌است.', code='duplicate_mother'
            )
        return super().clean()

    def save(self, commit=True):
        self.instance.gender = enums.GenderChoices.FEMALE
        mother = super().save(commit)
        self.person.mother = mother
        self.person.save()
        return mother


class PersonAddSpouseForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        spouse = super().save(commit)
        self.person.spouse.add(spouse)
        return spouse


class PersonAddChildForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        child = super().save(commit)
        if self.person.gender == enums.GenderChoices.MALE:
            child.father = self.person
        elif self.person.gender == enums.GenderChoices.FEMALE:
            child.mother = self.person
        child.save()
        return child


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
