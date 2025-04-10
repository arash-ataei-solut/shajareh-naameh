from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as j_models


class TicketCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('نام'))

    class Meta:
        verbose_name = _('دسته‌بندی تیکت')
        verbose_name_plural = _('دسته‌بندی‌های تیکت')

    def __str__(self):
        return self.name


class AnonymousTicket(models.Model):
    email = models.EmailField(verbose_name=_('ایمیل'))
    name = models.CharField(max_length=100, verbose_name=_('نام'))
    category = models.ForeignKey('common.TicketCategory', on_delete=models.PROTECT, verbose_name=_('دسته‌بندی'))
    description = models.TextField(verbose_name=_('شرح تیکت'))
    created_at = j_models.jDateTimeField(auto_now_add=True, verbose_name=_('زمان ایجاد'))
    answer = models.TextField(verbose_name=_('پاسخ تیکت'))
    answered_at = j_models.jDateTimeField(auto_now_add=True, verbose_name=_('زمان پاسخ'))

    class Meta:
        verbose_name = _('تیکت')
        verbose_name_plural = _('تیکت‌ها')
        ordering = ('created_at',)

    @property
    def answered(self):
        return self.answer is not None and len(self.answer) > 0

    @property
    def status(self):
        return _('پاسخ داده شده') if self.answered else _('در انتظار پاسخ')

    status.fget.short_description = _('وضعیت پاسخ')
