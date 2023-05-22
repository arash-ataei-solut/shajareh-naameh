from django.db import models
from django.utils.translation import gettext_lazy as _

from places.enums import PlaceTypeChoices


class Country(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('نام'))

    class Meta:
        verbose_name = _('کشور')
        verbose_name_plural = _('کشورها')

    def __str__(self):
        return self.name


class Province(models.Model):
    country = models.ForeignKey('places.Country', on_delete=models.CASCADE, verbose_name=_('کشور'))
    name = models.CharField(max_length=100, verbose_name=_('نام'))

    class Meta:
        verbose_name = _('استان')
        verbose_name_plural = _('استان‌ها')

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey('places.Province', on_delete=models.CASCADE, verbose_name=_('استان'))
    name = models.CharField(max_length=100, verbose_name=_('نام'))

    class Meta:
        verbose_name = _('شهرستان')
        verbose_name_plural = _('شهرستان‌ها')

    def __str__(self):
        return self.name


class Place(models.Model):
    city = models.ForeignKey('places.City', on_delete=models.CASCADE, verbose_name=_('شهرستان'))
    type = models.IntegerField(verbose_name=_('نوع'), choices=PlaceTypeChoices.choices)
    name = models.CharField(max_length=100, verbose_name=_('نام'))

    class Meta:
        verbose_name = _('مکان')
        verbose_name_plural = _('مکان‌ها')

    def __str__(self):
        return f'{self.city.province.country.name} - {self.city.province.name} - {self.name}'


class ResidencePlace(models.Model):
    place = models.ForeignKey('places.Place', on_delete=models.PROTECT, verbose_name=_('مکان'))
    from_year = models.SmallIntegerField(verbose_name=_('از سال'))
    to_year = models.SmallIntegerField(verbose_name=_('تا سال'))

    class Meta:
        verbose_name = _('محل سکونت')
        verbose_name_plural = _('محل‌های سکونت')
