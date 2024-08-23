from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.htmx.forms import PlaceholderFormMixin
from persons import enums
from persons.enums import RelationRequestStatusChoices, MatchingStatusChoices
from persons.matchmakers import RelationMatchmaker
from persons.models import Person, RelationMatchingRequest, SeeTreePermissionRequest
from places.forms import PlaceWidget
from places.models import ResidencePlace


class PersonAddForm(PlaceholderFormMixin, forms.ModelForm):
    created_by = forms.HiddenInput()

    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]

    def save(self, commit=True):
        instance: Person = super().save(commit)
        instance.can_see_tree_users.add(self.created_by)
        return instance


class PersonAddMyselfForm(PlaceholderFormMixin, forms.ModelForm):
    user = forms.HiddenInput()
    created_by = forms.HiddenInput()

    class Meta:
        model = Person
        fields = [
            'user', 'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]


class PersonUpdateForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year',
            'birth_date', 'birth_place', 'death_year', 'death_date'
        ]
        widgets = {
            'birth_place': PlaceWidget,
            'birth_date': forms.TextInput({'data-jdp': '', 'autocomplete': 'off'}),
            'death_date': forms.TextInput({'data-jdp': '', 'autocomplete': 'off'})
        }


class PersonAddResidenceForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = ResidencePlace
        fields = ['place', 'from_year', 'to_year']
        widgets = {
            'place': PlaceWidget,
        }

    def __init__(self, *args, **kwargs):
        self.person: Person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.person = self.person
        place: ResidencePlace = super().save(commit)
        return place


class PersonUpdateResidencePlaceForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = ResidencePlace
        fields = ['place', 'from_year', 'to_year']
        widgets = {
            'place': PlaceWidget,
        }


class PersonAddFatherForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person: Person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.person.father:
            raise ValidationError(
                'پدر این شخص ثبت شده‌است.', code='duplicate_mother'
            )
        return super().clean()

    def save(self, commit=True):
        self.instance.gender = enums.GenderChoices.MALE
        father: Person = super().save(commit)
        self.person.father = father
        self.person.save()
        if self.person.mother:
            father.spouses.add(self.person.mother)
        return father


class PersonAddMotherForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person: Person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.person.mother:
            raise ValidationError(
                'مادر این شخص ثبت شده‌است.', code='duplicate_mother'
            )
        return super().clean()

    def save(self, commit=True):
        self.instance.gender = enums.GenderChoices.FEMALE
        mother: Person = super().save(commit)
        self.person.mother = mother
        self.person.save()
        if self.person.father:
            mother.spouses.add(self.person.father)
        return mother


class PersonAddSpouseForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person: Person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        spouse: Person = super().save(commit)
        self.person.spouses.add(spouse)
        return spouse


class PersonAddChildForm(PlaceholderFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'last_name', 'gender', 'birth_year', 'created_by',
        ]

    def __init__(self, *args, **kwargs):
        self.person: Person = kwargs.pop('person')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        child: Person = super().save(commit)
        if self.person.gender == enums.GenderChoices.MALE:
            child.father = self.person
        elif self.person.gender == enums.GenderChoices.FEMALE:
            child.mother = self.person
        child.save()
        return child


class RelationRequestSetSimilarForm(forms.ModelForm):
    similar_related_person = forms.ModelChoiceField(queryset=Person.objects.all(), label=_('شخص مشابه'), required=False)

    class Meta:
        model = RelationMatchingRequest
        fields = ['similar_related_person']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        matchmaker = RelationMatchmaker(self.instance.related_person, self.instance.person, self.instance.relation)
        self.fields['similar_related_person'].queryset = matchmaker.queryset
        self.fields['similar_related_person'].choices = matchmaker.related_person_match_choices()

    def save(self, commit=True):
        if self.instance.similar_related_person is None:
            self.instance.status = RelationRequestStatusChoices.REJECTED_SIMILARITY
            self.instance.related_person.matching_status = MatchingStatusChoices.NO_MATCH
            self.instance.related_person.save()
        else:
            self.instance.status = RelationRequestStatusChoices.AWAITING_CONFIRMATION
        return super().save(commit)


class SeeTreePermissionRequestCreateForm(forms.ModelForm):
    class Meta:
        model = SeeTreePermissionRequest
        fields = ['person', 'applicant']

    def clean(self):
        cleaned_data = super().clean()
        person = cleaned_data['person']
        applicant = cleaned_data['applicant']
        request_exists = SeeTreePermissionRequest.objects.filter(
            person_id=person.id,
            applicant_id=applicant.id,
            status=enums.SeeTreePermissionRequestStatusChoices.AWAITING_APPROVE
        ).exists()
        if request_exists:
            raise ValidationError(
                'شما یک درخواست برای دریافت دسترسی مشاهده درخت‌خانوادگی این شخص ثبت کرده‌اید. '
                'لطغا منتظر تایید آن بمانید.'
            )
        return cleaned_data


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
