from django_select2.forms import ModelSelect2Widget


class PlaceWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains', 'city__name__icontains', 'city__province__name__icontains',
        'city__province__country__name__icontains'
    ]
