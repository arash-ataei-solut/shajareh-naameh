from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as j_models

from users.models import ShnUser
from . import managers
from .enums import GenderChoices, MatchingStatusChoices, RelationChoices, RelationRequestStatusChoices


class Person(models.Model):
    user = models.OneToOneField(
        'users.ShnUser', on_delete=models.SET_NULL,
        related_name='person',
        null=True, blank=True,
    )
    first_name = models.CharField(max_length=150, verbose_name=_('اسم'))
    last_name = models.CharField(max_length=150, verbose_name=_('فامیلی'))
    gender = models.IntegerField(verbose_name=_('جنسیت'), choices=GenderChoices.choices)
    father = models.ForeignKey(
        'self', on_delete=models.PROTECT,
        related_name='father_children',
        verbose_name=_('پدر'),
        null=True, blank=True
    )
    mother = models.ForeignKey(
        'self', on_delete=models.PROTECT,
        related_name='mother_children',
        verbose_name=_('مادر'),
        null=True, blank=True
    )
    spouses = models.ManyToManyField(
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

    created_by = models.ForeignKey(
        'users.ShnUser', on_delete=models.CASCADE,
        related_name='created_persons', related_query_name='created_person',
        verbose_name=_('ثبت شده توسط')
    )
    created_at = j_models.jDateTimeField(auto_now_add=True, verbose_name=_('زمان ایجاد'))
    updated_at = j_models.jDateTimeField(auto_now=True, verbose_name=_('زمان آخرین ویرایش'))

    matching_status = models.IntegerField(
        choices=MatchingStatusChoices.choices,
        default=MatchingStatusChoices.NO_MATCH,
        verbose_name=_('وضعیت تطابق')
    )

    objects = managers.PersonManager()

    class Meta:
        verbose_name = _('شخص')
        verbose_name_plural = _('اشخاص')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ancestors_id_list = []
        self.descendant_id_list = []

    def __str__(self):
        return f'{self.full_name} - {self.get_gender_display()} - {self.birth_year}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_matching(self):
        return bool(self.matching_status == MatchingStatusChoices.IS_MATCHING)

    def get_ancestors(self, main_person: 'Person' = None):
        main_person = main_person or self
        ancestors = {}
        if self.father and self.father.id not in self.ancestors_id_list:
            ancestors['father'] = {
                'id': self.father.id,
                'full_name': self.father.full_name,
                'ancestors': self.father.get_ancestors(main_person=main_person)
            }
            main_person.ancestors_id_list.append(self.father.id)
        if self.mother:
            ancestors['mother'] = {
                'id': self.mother.id,
                'full_name': self.mother.full_name,
                'ancestors': self.mother.get_ancestors()
            }
        return ancestors

    def get_descendant(self):
        descendant = []
        if hasattr(self, 'father_children'):
            children = self.father_children.all().only('id', 'first_name', 'last_name')
            for child in children:
                descendent



class RelationMatchingRequest(models.Model):
    person = models.ForeignKey(
        'persons.Person', on_delete=models.CASCADE,
        related_name='relation_requests', related_query_name='relation_request',
        verbose_name=_('شخص')
    )
    related_person = models.OneToOneField(
        'persons.Person', on_delete=models.CASCADE,
        related_name='relation_request_related',
        verbose_name=_('شخص وابسته')
    )
    similar_related_person = models.ForeignKey(
        'persons.Person', on_delete=models.CASCADE,
        related_name='relation_request_similar_related',
        verbose_name=_('شخص وابسته مشابه'),
        null=True, blank=True,
    )
    relation = models.CharField(max_length=10, choices=RelationChoices.choices, verbose_name=_('نسبت'))
    status = models.IntegerField(
        choices=RelationRequestStatusChoices.choices,
        default=RelationRequestStatusChoices.AWAITING_SIMILAR,
        verbose_name=_('وضعیت')
    )

    class Meta:
        verbose_name = _('درخواست تطابق وابستگان')
        verbose_name_plural = _('درخواست‌های تطابق وابستگان')

    @property
    def is_awaiting_similar(self):
        return bool(self.status == RelationRequestStatusChoices.AWAITING_SIMILAR)

    @property
    def is_awaiting_confirmation(self):
        return bool(self.status == RelationRequestStatusChoices.AWAITING_CONFIRMATION)
