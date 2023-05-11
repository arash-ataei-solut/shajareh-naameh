from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import GenderChoices
from django_jalali.db import models as j_models


class Person(models.Model):
    first_name = models.CharField(max_length=150, verbose_name=_('اسم'))
    last_name = models.CharField(max_length=150, verbose_name=_('فامیلی'))
    gender = models.IntegerField(verbose_name=_('جنسیت'), choices=GenderChoices.choices)
    father = models.ForeignKey(
        'self', on_delete=models.PROTECT,
        related_name='father_children',
        verbose_name=_('پدر')
    )
    mother = models.ForeignKey(
        'self', on_delete=models.PROTECT,
        related_name='mother_children',
        verbose_name=_('مادر')
    )
    spouse = models.ManyToManyField(
        'self',
        verbose_name=_('همسر'), blank=True
    )
    birth_year = models.SmallIntegerField(verbose_name=_('سال تولد'))
    birth_date = j_models.jDateField(verbose_name=_('تاریخ تولد'), null=True, blank=True)
    birth_place = models.ForeignKey(
        'places.Place', on_delete=models.PROTECT, verbose_name=_('محل تولد'), null=True, blank=True
    )
    residence_place = models.ManyToManyField(
        'places.ResidencePlace', verbose_name=_('محل سکونت'), blank=True
    )
    death_year = models.SmallIntegerField(verbose_name=_('سال وفات'), null=True, blank=True)
    death_date = j_models.jDateField(verbose_name=_('تاریخ وفات'), null=True, blank=True)

    class Meta:
        verbose_name = _('شخص')
        verbose_name_plural = _('اشخاص')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.father.first_name}'
