from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MobileNumberValidator(validators.RegexValidator):
    regex = r'^(?:[۰][۹]|[0][9])(?:[۰-۹]|[0-9]){9}$'
    message = _(
        'یک شماره موبایل معتبر وارد کنید.'
    )
    flags = 0


class OTPValidator(validators.RegexValidator):
    regex = r'\d+$'
    message = 'لطفا فقط عدد وارد کنید.'
