from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, FormView, ListView, TemplateView
from django_htmx.http import HttpResponseClientRedirect

from common.mixins import HTMXViewMixin, HTMXFormViewMixin
from persons.enums import RelationMatchingRequestStatusChoices
from persons.models import RelationMatchingRequest, Person
from users import enums
from users.exeptions import SendOTPError
from users.forms import LoginForm, RegisterForm, ConfirmOTPForm, ResetPasswordForm, ConfirmResetPasswordForm
from users.models import ShnUser, Notification

OTP_USER_SESSION = 'registered_user_id'
RESET_PASSWORD_USER_SESSION = 'reset_password_user_id'


class ShnLoginView(HTMXFormViewMixin, LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    htmx_template_name = 'registration/htmx/login_htmx.html'
    redirect_authenticated_user = False
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.get_user()
        if not user.has_valid_otp(usage=enums.OTPUsageChoices.REGISTER):
            self.request.session[OTP_USER_SESSION] = str(user.id)
            return HttpResponseRedirect(reverse('users:send-otp-login'))

        auth_login(self.request, form.get_user())
        return super().form_valid(form)


class RegisterView(HTMXViewMixin, CreateView):
    model = ShnUser
    form_class = RegisterForm
    template_name = 'registration/register.html'
    htmx_template_name = 'registration/htmx/register_htmx.html'
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
        kwargs = super().get_form_kwargs()
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
        return super().form_valid(form)


class ConfirmRegisterOTPView(ConfirmOTOViewMixin, HTMXFormViewMixin, FormView):
    usage = enums.OTPUsageChoices.REGISTER
    template_name = 'registration/confirm_register.html'
    htmx_template_name = 'registration/htmx/confirm_register_htmx.html'
    success_url = reverse_lazy('users:login')


class SendLoginOTPView(SendOTPView):
    usage = enums.OTPUsageChoices.REGISTER
    confirm_otp_url = reverse_lazy('users:confirm-login')


class ConfirmLoginOTPView(ConfirmOTOViewMixin, HTMXFormViewMixin, FormView):
    usage = enums.OTPUsageChoices.REGISTER
    template_name = 'registration/confirm_login.html'
    htmx_template_name = 'registration/htmx/confirm_login_htmx.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super(ConfirmLoginOTPView, self).form_valid(form)
        auth_login(self.request, form.user)
        return response


class ResetPasswordView(HTMXViewMixin, FormView):
    form_class = ResetPasswordForm
    template_name = 'registration/reset_password.html'
    htmx_template_name = 'registration/htmx/reset_password_htmx.html'
    success_url = reverse_lazy('users:send-otp-reset-password')

    def form_valid(self, form):
        response = super(ResetPasswordView, self).form_valid(form)
        registered_user_id = form.get_user_id()
        self.request.session[OTP_USER_SESSION] = registered_user_id
        return response


class SendResetPasswordOTPView(SendOTPView):
    usage = enums.OTPUsageChoices.RESET_PASSWORD
    confirm_otp_url = reverse_lazy('users:confirm-reset-password-otp')


class ConfirmResetPasswordOTPView(ConfirmOTOViewMixin, HTMXFormViewMixin, FormView):
    usage = enums.OTPUsageChoices.RESET_PASSWORD
    template_name = 'registration/confirm_reset_password_otp.html'
    htmx_template_name = 'registration/htmx/confirm_reset_password_otp_htmx.html'
    success_url = reverse_lazy('users:confirm-reset-password')
    
    def form_valid(self, form):
        registered_user_id = self.request.session.get(OTP_USER_SESSION)
        self.request.session[RESET_PASSWORD_USER_SESSION] = registered_user_id
        return super(ConfirmResetPasswordOTPView, self).form_valid(form)


class ConfirmResetPasswordView(HTMXViewMixin, FormView):
    form_class = ConfirmResetPasswordForm
    template_name = 'registration/confirm_reset_password.html'
    htmx_template_name = 'registration/htmx/confirm_reset_password_htmx.html'
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


class PersonalInfoProfileView(LoginRequiredMixin, HTMXViewMixin, TemplateView):
    model = ShnUser
    template_name = 'profile/personal_info_profile.html'
    htmx_template_name = 'profile/htmx/person_info_profile_htmx.html'

    def get_context_data(self, **kwargs):
        context = super(PersonalInfoProfileView, self).get_context_data(**kwargs)
        context.update({'person': getattr(self.request.user, 'person', None)})
        return context


class NotificationsListProfileView(LoginRequiredMixin, HTMXViewMixin, ListView):
    model = Notification
    template_name = 'profile/notifications_list_profile.html'
    htmx_template_name = 'profile/htmx/notifications_list_profile_htmx.html'

    def get_queryset(self):
        return self.request.user.notification_set.all()


class ChangePasswordView(HTMXViewMixin, PasswordChangeView):
    template_name = 'profile/change_password_profile.html'
    success_url = reverse_lazy('users:change-password-done-profile')
    htmx_template_name = 'profile/htmx/change_password_profile_htmx.html'


class ChangePasswordDoneView(HTMXViewMixin, PasswordChangeDoneView):
    template_name = 'profile/change_password_done_profile.html'
    htmx_template_name = 'profile/htmx/change_password_done_profile_htmx.html'


class PersonListView(LoginRequiredMixin, HTMXViewMixin, ListView):
    template_name = 'profile/person_list.html'
    htmx_template_name = 'profile/htmx/person_list_htmx.html'
    paginate_by = 5

    def get_queryset(self):
        return Person.objects.exclude_matched_persons().filter(created_by=self.request.user)


class RelationMatchingRequestListView(LoginRequiredMixin, HTMXViewMixin, ListView):
    template_name = 'profile/relation_matching_request_list.html'
    htmx_template_name = 'profile/htmx/relation_matching_request_list_htmx.html'

    def get_queryset(self):
        return RelationMatchingRequest.objects.filter(similar_related_person__created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'status_choices': RelationMatchingRequestStatusChoices})
        return context


class MyRelationMatchingRequestListView(LoginRequiredMixin, HTMXViewMixin, ListView):
    template_name = 'profile/my_relation_matching_request_list.html'
    htmx_template_name = 'profile/htmx/my_relation_matching_request_list_htmx.html'

    def get_queryset(self):
        return RelationMatchingRequest.objects.filter(related_person__created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({'status_choices': RelationMatchingRequestStatusChoices})
        return context
