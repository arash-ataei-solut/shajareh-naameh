from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from common.htmx.forms import PlaceholderFormMixin
from users import enums
from users.exeptions import OTPDoesNotExist, OTPExpired, OTPIsInvalid
from users.models import ShnUser
from users.validators import MobileNumberValidator


class LoginForm(PlaceholderFormMixin, AuthenticationForm):
    pass


class RegisterForm(PlaceholderFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShnUser
        fields = ('mobile', )
        field_classes = {"mobile": UsernameField}

    def get_user_id(self) -> str:
        return str(self.instance.id)


class ConfirmOTPForm(PlaceholderFormMixin, forms.Form):
    otp = forms.CharField(max_length=5, min_length=5, label=_('رمز یک‌بارمصرف'))

    def __init__(self, user, usage, **kwargs):
        super(ConfirmOTPForm, self).__init__(**kwargs)
        self.user = user
        self.usage = usage

    def clean_otp(self):
        entered_otp = self.cleaned_data['otp']
        try:
            self.user.check_otp(self.usage, entered_otp)
        except (OTPDoesNotExist, OTPExpired):
            raise ValidationError(_('لطفا یک رمز یک‌بارمصرف جدید دریافت کنید.'))
        except OTPIsInvalid:
            raise ValidationError(_('رمز یک‌بارمصرف وارد شده صحیح نیست.'))

        return entered_otp

    def confirm(self):
        self.user.confirm_otp(self.usage)


class ResetPasswordForm(PlaceholderFormMixin, forms.Form):
    mobile_validator = MobileNumberValidator()
    mobile = forms.CharField(validators=[mobile_validator], label=_('شماره موبایل'))

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        try:
            self.user = ShnUser.objects.get(mobile=mobile)
        except ShnUser.DoesNotExist:
            raise ValidationError(_('شماره موبایل وارد شده در سامانه ثبت نشده‌است.'))
        return mobile

    def get_user_id(self) -> str:
        return str(self.user.id)


class ConfirmResetPasswordForm(PlaceholderFormMixin, SetPasswordForm):
    
    def clean(self):
        if not self.user.has_valid_otp(enums.OTPUsageChoices.RESET_PASSWORD):
            raise ValidationError(_('شماره موبایل شما تایید نشده است.'))
        return super(ConfirmResetPasswordForm, self).clean()


class PersonalInfoProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ShnUser
        fields = ['national_code']

