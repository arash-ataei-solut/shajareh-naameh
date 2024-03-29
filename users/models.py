import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as j_models

from . import enums
from .exeptions import SendOTPError, OTPDoesNotExist, OTPExpired, OTPIsInvalid
from .managers import AuthOTPManager
from .validators import MobileNumberValidator


class ShnUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile_validator = MobileNumberValidator()
    mobile = models.CharField(
        _('شماره موبایل'),
        max_length=11,
        unique=True,
        validators=[mobile_validator],
        error_messages={
            'unique': _("کاربری با این شماره موبایل موجود است."),
        },
    )
    type = models.IntegerField(
        verbose_name=_('نوع کاربر'), choices=enums.UserTypeChoices.choices, default=enums.UserTypeChoices.NORMAL
    )
    image = models.ImageField(verbose_name=_('عکس'), null=True, blank=True)

    USERNAME_FIELD = 'mobile'

    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    def __str__(self):
        return self.mobile

    def send_otp(self, usage: enums.OTPUsageChoices):
        unexpired_otp_time = timezone.now() - timezone.timedelta(minutes=settings.OTP_EXP_MINUTES)
        unexpired_otp_exists = self.authotp_set.filter(
            usage=usage, confirmed=False, created_at__gt=unexpired_otp_time
        ).exists()
        if unexpired_otp_exists:
            raise SendOTPError()

        otp = AuthOTP.objects.create_otp(user=self, usage=usage)
        otp.send_by_sms()

    def check_otp(self, usage: enums.OTPUsageChoices, otp_code: str):
        unexpired_otp_time = timezone.now() - timezone.timedelta(minutes=settings.OTP_EXP_MINUTES)
        try:
            otp = self.authotp_set.filter(
                usage=usage, confirmed=False, created_at__gt=unexpired_otp_time
            ).latest('created_at')
        except AuthOTP.DoesNotExist:
            raise OTPDoesNotExist()

        if otp.expired or otp.attempts > 3:
            raise OTPExpired()

        if otp.code != otp_code:
            otp.attempts += 1
            otp.save()
            raise OTPIsInvalid()

    def confirm_otp(self, usage: enums.OTPUsageChoices):
        otp = self.authotp_set.filter(usage=usage).latest('created_at')
        otp.confirmed = True
        otp.save()

    def has_valid_otp(self, usage: enums.OTPUsageChoices, validity_minutes: int = settings.OTP_VALIDITY_MINUTES):
        validity_period = timezone.now() - timezone.timedelta(minutes=validity_minutes)
        return self.authotp_set.filter(confirmed=True, usage=usage, created_at__gt=validity_period).exists()


class AuthOTP(models.Model):
    user = models.ForeignKey('users.ShnUser', on_delete=models.CASCADE, verbose_name=_('کاربر'))
    usage = models.CharField(max_length=2, verbose_name=_('کاربرد'), choices=enums.OTPUsageChoices.choices)
    code = models.CharField(max_length=5, verbose_name=_('رمز یک‌بارمصرف'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('زمان ایجاد'))
    attempts = models.PositiveSmallIntegerField(verbose_name=_('تعداد تلاش'), default=0)
    confirmed = models.BooleanField(verbose_name=_('تایید شده'), default=False)

    objects = AuthOTPManager()

    class Meta:
        verbose_name = _('رمز یک‌بارمصرف')
        verbose_name_plural = _('رمز‌های یک‌بارمصرف')
        ordering = ('created_at', )

    @property
    def expired(self) -> bool:
        expiration_time = self.created_at + timezone.timedelta(minutes=settings.OTP_EXP_MINUTES)
        return timezone.now() > expiration_time

    def send_by_sms(self):
        print(self.code)


class Notification(models.Model):
    user = models.ForeignKey('users.ShnUser', on_delete=models.CASCADE, verbose_name=_('کاربر'))
    title = models.CharField(max_length=40, verbose_name=_('عنوان'))
    content = models.TextField(verbose_name=_('محتوا'))
    seen = models.BooleanField(verbose_name=_('خوانده شده'), default=False)
    created_at = j_models.jDateTimeField(auto_now_add=True, verbose_name=_('زمان ایجاد'))

    class Meta:
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلان‌ها')

    def __str__(self):
        return self.title
