from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as j_models

from users.models import ShnUser
from . import managers, enums
from .exceptions import LoopInTreeException


class SeeTreePermissionRequest(models.Model):
    person = models.ForeignKey(
        'persons.Person', on_delete=models.CASCADE,
        verbose_name=_('شخص'),
        help_text=_('شخصی که کاربر میخواهد دسترسی مشاهده درخت‌خانوادگی او را داشته باشد.')
    )
    applicant = models.ForeignKey(
        'users.ShnUser', on_delete=models.CASCADE,
        verbose_name=_('کاربر متقاضی')
    )
    status = models.IntegerField(
        choices=enums.SeeTreePermissionRequestStatusChoices.choices,
        default=enums.SeeTreePermissionRequestStatusChoices.AWAITING_APPROVE,
        verbose_name=_('وضعیت'),
    )
    created_at = j_models.jDateTimeField(auto_now=True, verbose_name=_('زمان ایجاد'))

    class Meta:
        verbose_name = _('درخواست دریافت دسترسی مشاهده درخت‌خانوادگی')
        verbose_name_plural = _('درخواست‌های دریافت دسترسی مشاهده درخت‌خانوادگی')


class Person(models.Model):
    user = models.OneToOneField(
        'users.ShnUser', on_delete=models.SET_NULL,
        related_name='person',
        null=True, blank=True,
    )
    first_name = models.CharField(max_length=150, verbose_name=_('اسم'))
    last_name = models.CharField(max_length=150, verbose_name=_('فامیلی'))
    gender = models.IntegerField(verbose_name=_('جنسیت'), choices=enums.GenderChoices.choices)
    father = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        related_name='father_children',
        verbose_name=_('پدر'),
        null=True, blank=True
    )
    mother = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
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
        choices=enums.MatchingStatusChoices.choices,
        default=enums.MatchingStatusChoices.NO_MATCH,
        verbose_name=_('وضعیت تطابق')
    )

    can_see_tree_users = models.ManyToManyField(
        'users.ShnUser',
        related_name='can_see_persons_tree',
        verbose_name=_('کاربرانی که می‌توانند درخت‌خانوادگی این شخص را ببینند.')
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
        return bool(self.matching_status == enums.MatchingStatusChoices.IS_MATCHING)

    def get_ancestors(self, main_person: 'Person' = None):
        main_person = main_person or self
        ancestors = {}
        if self.father:
            if self.father.id in self.ancestors_id_list:
                raise LoopInTreeException()
            ancestors['father'] = {
                'id': self.father.id,
                'full_name': self.father.full_name,
                'ancestors': self.father.get_ancestors(main_person=main_person)
            }
            main_person.ancestors_id_list.append(self.father.id)
        if self.mother:
            if self.mother.id in self.ancestors_id_list:
                raise LoopInTreeException()
            ancestors['mother'] = {
                'id': self.mother.id,
                'full_name': self.mother.full_name,
                'ancestors': self.mother.get_ancestors(main_person=main_person)
            }
            main_person.ancestors_id_list.append(self.mother.id)
        return ancestors

    def get_descendant(self, main_person: 'Person' = None):
        main_person = main_person or self
        descendant = []
        children = Person.objects.filter(
            Q(father_id=self.id) | Q(mother_id=self.id)
        ).only('id', 'first_name', 'last_name', 'gender')
        for child in children:
            if child.id in main_person.descendant_id_list:
                raise LoopInTreeException()
            descendant.append(
                {
                    'id': child.id,
                    'full_name': child.full_name,
                    'gender': child.get_gender_display(),
                    'descendant': child.get_descendant(main_person=main_person)
                }
            )
            main_person.descendant_id_list.append(child.id)
        return descendant

    def can_see_tree(self, user: ShnUser) -> bool:
        return self.can_see_tree_users.filter(id=user.id).exists()

    def can_update(self, user: ShnUser) -> bool:
        return self.created_by == user or self.user == user

    def has_awaiting_see_tree_request(self, user: ShnUser) -> bool:
        return SeeTreePermissionRequest.objects.filter(
            person_id=self.id,
            applicant_id=user.id,
            status=enums.SeeTreePermissionRequestStatusChoices.AWAITING_APPROVE
        )


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
    relation = models.CharField(max_length=10, choices=enums.RelationChoices.choices, verbose_name=_('نسبت'))
    status = models.IntegerField(
        choices=enums.RelationRequestStatusChoices.choices,
        default=enums.RelationRequestStatusChoices.AWAITING_SIMILAR,
        verbose_name=_('وضعیت')
    )

    created_by = models.ForeignKey(
        'users.ShnUser', on_delete=models.CASCADE,
        related_name='created_relation_matching_requests',
        related_query_name='created_relation_matching_request',
        verbose_name=_('ثبت شده توسط')
    )
    created_at = j_models.jDateTimeField(auto_now_add=True, verbose_name=_('زمان ایجاد'))
    updated_at = j_models.jDateTimeField(auto_now=True, verbose_name=_('زمان آخرین ویرایش'))

    class Meta:
        verbose_name = _('درخواست تطابق وابستگان')
        verbose_name_plural = _('درخواست‌های تطابق وابستگان')

    @property
    def is_awaiting_similar(self):
        return bool(self.status == enums.RelationRequestStatusChoices.AWAITING_SIMILAR)

    @property
    def is_awaiting_confirmation(self):
        return bool(self.status == enums.RelationRequestStatusChoices.AWAITING_CONFIRMATION)

    def do_the_match(self):
        self.status = enums.RelationRequestStatusChoices.MATCHING_IS_DONE
        self.related_person.matching_status = enums.MatchingStatusChoices.MATCHED
        if self.relation == enums.RelationChoices.FATHER:
            self.person.father = self.similar_related_person
        elif self.relation == enums.RelationChoices.MOTHER:
            self.person.mother = self.similar_related_person
        self.person.save()
        if self.relation == enums.RelationChoices.CHILD:
            if self.person.gender == enums.GenderChoices.MALE:
                self.similar_related_person.father = self.person
            elif self.person.gender == enums.GenderChoices.FEMALE:
                self.similar_related_person.mother = self.person
            self.similar_related_person.save()
        if self.relation == enums.RelationChoices.SPOUSE:
            self.person.spouses.add(self.similar_related_person)

    def reject_the_match(self):
        self.status = enums.RelationRequestStatusChoices.REJECTED_SIMILARITY
        self.related_person.matching_status = enums.MatchingStatusChoices.NO_MATCH
