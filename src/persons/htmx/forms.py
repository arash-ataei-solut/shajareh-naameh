from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.utils.translation import gettext as _

from persons.models import Person


class AddMyPersonForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AddMyPersonForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'gender']
        widgets = {
            'first_name': TextInput
        }

    def clean(self):
        if hasattr(self.user, 'person'):
            raise ValidationError(_('اطلاعات شخصی شما موجود است.'))
        return self.cleaned_data
