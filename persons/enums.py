from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class GenderChoices(IntegerChoices):
    MALE = 1, _('مرد')
    FEMALE = 2, _('زن')


class MatchingStatusChoices(IntegerChoices):
    NO_MATCH = 0, _('بدون انطباق')
    MATCHING = 1, _('در حال تطابق')
    MATCHED = 2, _('تطابق یافته')


class RelationChoices(TextChoices):
    FATHER = 'FATHER', _('پدر')
    MOTHER = 'MOTHER', _('مادر')
    SPOUSE = 'SPOUSE', _('همسر')
    CHILD = 'CHILD', _('فرزند')
