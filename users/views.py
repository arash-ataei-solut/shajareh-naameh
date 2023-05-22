from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, resolve_url
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, FormView, DetailView

from users import enums
from users.exeptions import SendOTPError
from users.forms import LoginForm, RegisterForm, ConfirmOTPForm, ResetPasswordForm, ConfirmResetPasswordForm
from users.models import ShnUser

OTP_USER_SESSION = 'registered_user_id'
RESET_PASSWORD_USER_SESSION = 'reset_password_user_id'


class ShnLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    send_otp_url = reverse_lazy('users:send-otp-login')
    redirect_authenticated_user = True

    def success_response(self):
        return HttpResponseRedirect(self.get_success_url())

    def confirm_required_response(self):
        return HttpResponseRedirect(str(self.send_otp_url))

    def form_valid(self, form):
        user = form.get_user()
        if not user.has_valid_otp(usage=enums.OTPUsageChoices.REGISTER):
            self.request.session[OTP_USER_SESSION] = str(user.id)
            return self.confirm_required_response()

        auth_login(self.request, form.get_user())
        return self.success_response()


class RegisterView(CreateView):
    model = ShnUser
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('users:send-otp-register')

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        registered_user_id = form.get_user_id()
        self.request.session[OTP_USER_SESSION] = registered_user_id
        return response


class SendOTPView(View):
    usage: enums.OTPUsageChoices = None
    confirm_otp_url = None

    def get_usage(self):
        if self.usage is None:
            raise ImproperlyConfigured(
                'SendOTPView requires a definition of otp usage.'
            )
        return self.usage

    def get_confirm_otp_url(self):
        if self.confirm_otp_url is None:
            raise ImproperlyConfigured(
                'No otp confirm form url to redirect to. add otp confirm form view and use its url.'
            )
        return self.confirm_otp_url

    def get_user_from_session(self):
        registered_user_id = self.request.session.get(OTP_USER_SESSION)
        return get_object_or_404(ShnUser, pk=registered_user_id)

    def get(self, request):
        registered_user = self.get_user_from_session()
        try:
            registered_user.send_otp(self.get_usage())
            messages.success(request, _('رمز یک‌بارمصرف به موبایل شما ارسال شد.'), extra_tags='success')
        except SendOTPError:
            messages.error(
                request,
                _('ارسال رمز یک‌بارمصرف با خطا روبرو شد. لطفا لحظاتی بعد دوباره تلاش کنید.'),
                extra_tags='danger'
            )
        return HttpResponseRedirect(self.get_confirm_otp_url())


class SendRegisterOTPView(SendOTPView):
    usage = enums.OTPUsageChoices.REGISTER
    confirm_otp_url = reverse_lazy('users:confirm-register')


class ConfirmOTOViewMixin:
    usage: enums.OTPUsageChoices = None
    form_class = ConfirmOTPForm

    def get_usage(self):
        if self.usage is None:
            raise ImproperlyConfigured(
                'ConfirmOTOViewMixin requires a definition of otp usage.'
            )
        return self.usage

    def get_user_from_session(self):
        registered_user_id = self.request.session.get(OTP_USER_SESSION)
        return get_object_or_404(ShnUser, pk=registered_user_id)

    def get_form_kwargs(self):
        kwargs = super(ConfirmOTOViewMixin, self).get_form_kwargs()
        kwargs.update(
            {
                'user': self.get_user_from_session(),
                'usage': self.get_usage()
            }
        )
        return kwargs

    def form_valid(self, form):
        form.confirm()
        self.request.session.pop(OTP_USER_SESSION)
        return super(ConfirmOTOViewMixin, self).form_valid(form)


class ConfirmRegisterOTPView(ConfirmOTOViewMixin, FormView):
    usage = enums.OTPUsageChoices.REGISTER
    template_name = 'confirm_register.html'
    success_url = reverse_lazy('users:login')


class SendLoginOTPView(SendOTPView):
    usage = enums.OTPUsageChoices.REGISTER
    confirm_otp_url = reverse_lazy('users:confirm-login')


class ConfirmLoginOTPView(ConfirmOTOViewMixin, FormView):
    usage = enums.OTPUsageChoices.REGISTER
    template_name = 'confirm_login.html'

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def success_response(self):
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        super(ConfirmLoginOTPView, self).form_valid(form)
        auth_login(self.request, form.user)
        return self.success_response()


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'reset_password.html'
    success_url = reverse_lazy('users:send-otp-reset-password')

    def form_valid(self, form):
        response = super(ResetPasswordView, self).form_valid(form)
        registered_user_id = form.get_user_id()
        self.request.session[OTP_USER_SESSION] = registered_user_id
        return response


class SendResetPasswordOTPView(SendOTPView):
    usage = enums.OTPUsageChoices.RESET_PASSWORD
    confirm_otp_url = reverse_lazy('users:confirm-reset-password-otp')


class ConfirmResetPasswordOTPView(ConfirmOTOViewMixin, FormView):
    usage = enums.OTPUsageChoices.RESET_PASSWORD
    template_name = 'confirm_reset_password_otp.html'
    success_url = reverse_lazy('users:confirm-reset-password')
    
    def form_valid(self, form):
        registered_user_id = self.request.session.get(OTP_USER_SESSION)
        self.request.session[RESET_PASSWORD_USER_SESSION] = registered_user_id
        return super(ConfirmResetPasswordOTPView, self).form_valid(form)


class ConfirmResetPasswordView(FormView):
    form_class = ConfirmResetPasswordForm
    template_name = 'confirm_reset_password.html'
    success_url = reverse_lazy('users:login')

    def get_user_from_session(self):
        reset_password_user_id = self.request.session.get(RESET_PASSWORD_USER_SESSION)
        return get_object_or_404(ShnUser, pk=reset_password_user_id)

    def get_form_kwargs(self):
        kwargs = super(ConfirmResetPasswordView, self).get_form_kwargs()
        kwargs.update(
            {
                'user': self.get_user_from_session(),
            }
        )
        return kwargs
    
    def form_valid(self, form):
        form.save()
        self.request.session.pop(RESET_PASSWORD_USER_SESSION)
        return super(ConfirmResetPasswordView, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = ShnUser
    template_name = 'profile/user_profile_base.html'

    def get_object(self, queryset=None):
        return self.request.user


class PersonalInfoProfileView(LoginRequiredMixin, DetailView):
    model = ShnUser
    template_name = 'profile/personal_info_profile.html'

    def get_object(self, queryset=None):
        return self.request.user
