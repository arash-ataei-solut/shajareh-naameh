from django import forms

from common.models import AnonymousTicket


class PlaceholderFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label


class AnonymousTicketForm(PlaceholderFormMixin, forms.ModelForm):

    class Meta:
        model = AnonymousTicket
        fields = ['email', 'name', 'category', 'description', ]
