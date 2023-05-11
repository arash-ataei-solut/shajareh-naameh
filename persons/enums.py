from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class GenderChoices(IntegerChoices):
    MALE = 1, _('مرد')
    FEMALE = 2, _('زن')
