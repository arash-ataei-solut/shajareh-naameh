from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django_htmx.http import HttpResponseClientRefresh

from users import views as user_views
from users.models import Notification, ShnUser


class ShnLoginHTMXView(user_views.ShnLoginView):
    template_name = 'registration/htmx/login_htmx.html'
    send_otp_url = reverse_lazy('users:users-hx:send-otp-login-htmx')
    redirect_authenticated_user = False

    def success_response(self):
        return HttpResponseClientRefresh()


class RegisterHTMXView(user_views.RegisterView):
    template_name = 'registration/htmx/register_htmx.html'
    success_url = reverse_lazy('users:users-hx:send-otp-register-htmx')


class SendOTPRegisterHTMXView(user_views.SendRegisterOTPView):
    confirm_otp_url = reverse_lazy('users:users-hx:confirm-register-htmx')


class ConfirmRegisterHTMXView(user_views.ConfirmRegisterOTPView):
    template_name = 'registration/htmx/confirm_register_htmx.html'
    success_url = reverse_lazy('users:users-hx:login-htmx')


class SendOTPLoginHTMXView(user_views.SendLoginOTPView):
    confirm_otp_url = reverse_lazy('users:users-hx:confirm-login-htmx')


class ConfirmLoginHTMXView(user_views.ConfirmLoginOTPView):
    template_name = 'registration/htmx/confirm_login_htmx.html'

    def success_response(self):
        return HttpResponseClientRefresh()


class ResetPasswordHTMXView(user_views.ResetPasswordView):
    template_name = 'registration/htmx/reset_password_htmx.html'
    success_url = reverse_lazy('users:users-hx:send-otp-reset-password-htmx')


class SendOTPResetPasswordHTMXView(user_views.SendResetPasswordOTPView):
    confirm_otp_url = reverse_lazy('users:users-hx:confirm-reset-password-otp-htmx')


class ConfirmResetPasswordOTPHTMXView(user_views.ConfirmResetPasswordOTPView):
    template_name = 'registration/htmx/confirm_reset_password_otp_htmx.html'
    success_url = reverse_lazy('users:users-hx:confirm-reset-password-htmx')


class ConfirmResetPasswordHTMXView(user_views.ConfirmResetPasswordView):
    template_name = 'registration/htmx/confirm_reset_password_htmx.html'
    success_url = reverse_lazy('users:users-hx:login-htmx')


class UnreadNotificationsIconHTMXView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'registration/htmx/unread_notifications_icon_htmx.html'

    def get_queryset(self):
        queryset = self.request.user.unread_notifications()
        self.extra_context = {'object_list_count': queryset.count()}
        return queryset


class UnreadNotificationsHTMXView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'registration/htmx/unread_notifications_htmx.html'

    def get_queryset(self):
        pk_list = list(self.request.user.unread_notifications().values_list('pk', flat=True))
        queryset = Notification.objects.filter(pk__in=pk_list)
        queryset.update(read=True)
        self.extra_context = {'object_list_count': queryset.count()}
        return queryset


class PersonalInfoProfileHTMXView(LoginRequiredMixin, TemplateView):
    model = ShnUser
    template_name = 'profile/personal_info_profile.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalInfoProfileHTMXView, self).get_context_data(**kwargs)
        context.update({'person': getattr(self.request.user, 'person', None)})
        return context


class NotificationsListProfileHTMXView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'profile/notifications_list_profile.html'

    def get_queryset(self):
        return self.request.user.notification_set.all()


class ChangePasswordHTMXView(PasswordChangeView):
    template_name = 'profile/change_password_profile.html'
    success_url = reverse_lazy('users:change-password-done-profile')


class ChangePasswordDoneHTMXView(PasswordChangeDoneView):
    template_name = 'profile/change_password_done_profile.html'
