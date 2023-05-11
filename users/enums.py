from django.db import models
from django.utils.translation import gettext_lazy as _


class UserTypeChoices(models.IntegerChoices):
    NORMAL = 0, _('کاربر معمولی')
    APPROVER = 1, _('کاربر تایید کننده')
    SUBMITTER = 2, _('کاربر ثبت کننده')


class OTPUsageChoices(models.TextChoices):
    REGISTER = 'RG', _('ثبت‌نام')
    RESET_PASSWORD = 'RP', _('فراموشی رمز‌عبور')
