from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class PlaceTypeChoices(IntegerChoices):
    TOWN = 1, _('شهرستان')
    VILLAGE = 2, _('روستا')
