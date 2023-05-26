from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django_htmx.http import HttpResponseClientRefresh

from users import views as user_views
from users.forms import PersonalInfoProfileUpdateForm
from users.models import ShnUser


class ShnLoginHTMXView(user_views.ShnLoginView):
    template_name = 'htmx/login_htmx.html'
    send_otp_url = reverse_lazy('users:users-hx:send-otp-login-htmx')
    redirect_authenticated_user = False

    def success_response(self):
        return HttpResponseClientRefresh()


class RegisterHTMXView(user_views.RegisterView):
    template_name = 'htmx/register_htmx.html'
    success_url = reverse_lazy('users:users-hx:send-otp-register-htmx')


class SendOTPRegisterHTMXView(user_views.SendRegisterOTPView):
    confirm_otp_url = reverse_lazy('users:users-hx:confirm-register-htmx')


class ConfirmRegisterHTMXView(user_views.ConfirmRegisterOTPView):
    template_name = 'htmx/confirm_register_htmx.html'
    success_url = reverse_lazy('users:users-hx:login-htmx')


class SendOTPLoginHTMXView(user_views.SendLoginOTPView):
    confirm_otp_url = reverse_lazy('users:users-hx:confirm-login-htmx')


class ConfirmLoginHTMXView(user_views.ConfirmLoginOTPView):
    template_name = 'htmx/confirm_login_htmx.html'

    def success_response(self):
        return HttpResponseClientRefresh()


class ResetPasswordHTMXView(user_views.ResetPasswordView):
    template_name = 'htmx/reset_password_htmx.html'
    success_url = reverse_lazy('users:users-hx:send-otp-reset-password-htmx')


class SendOTPResetPasswordHTMXView(user_views.SendResetPasswordOTPView):
    confirm_otp_url = reverse_lazy('users:users-hx:confirm-reset-password-otp-htmx')


class ConfirmResetPasswordOTPHTMXView(user_views.ConfirmResetPasswordOTPView):
    template_name = 'htmx/confirm_reset_password_otp_htmx.html'
    success_url = reverse_lazy('users:users-hx:confirm-reset-password-htmx')


class ConfirmResetPasswordHTMXView(user_views.ConfirmResetPasswordView):
    template_name = 'htmx/confirm_reset_password_htmx.html'
    success_url = reverse_lazy('users:users-hx:login-htmx')


class PersonalInfoProfileUpdateView(UpdateView):
    model = ShnUser
    form_class = PersonalInfoProfileUpdateForm
    template_name = 'profile/htmx/update_personal_info_profile_htmx.html'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseClientRefresh()
