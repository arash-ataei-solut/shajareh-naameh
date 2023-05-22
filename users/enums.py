from django.db import models
from django.utils.translation import gettext_lazy as _


class OTPUsageChoices(models.TextChoices):
    REGISTER = 'RG', _('ثبت‌نام')
    RESET_PASSWORD = 'RP', _('فراموشی رمز‌عبور')
