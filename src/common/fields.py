from django.forms import fields


class SearchableSelect(fields.Select):
    template_name = 'fields/searchable_select.html'
