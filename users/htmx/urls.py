from django.urls import path

from . import views as users_htmx_views

app_name = 'users-hx'

urlpatterns = [
    path('login-htmx/', users_htmx_views.ShnLoginHTMXView.as_view(), name='login-htmx'),
    path('register-htmx/', users_htmx_views.RegisterHTMXView.as_view(), name='register-htmx'),
    path('send-otp-register-htmx/', users_htmx_views.SendOTPRegisterHTMXView.as_view(), name='send-otp-register-htmx'),
    path('confirm-register-htmx/', users_htmx_views.ConfirmRegisterHTMXView.as_view(), name='confirm-register-htmx'),
    path('send-otp-login-htmx/', users_htmx_views.SendOTPLoginHTMXView.as_view(), name='send-otp-login-htmx'),
    path('confirm-login-htmx/', users_htmx_views.ConfirmLoginHTMXView.as_view(), name='confirm-login-htmx'),
    path('reset-password-htmx/', users_htmx_views.ResetPasswordHTMXView.as_view(), name='reset-password-htmx'),
    path(
        'send-otp-reset-password-htmx/',
        users_htmx_views.SendOTPResetPasswordHTMXView.as_view(),
        name='send-otp-reset-password-htmx'
    ),
    path(
        'confirm-reset-password-otp-htmx/',
        users_htmx_views.ConfirmResetPasswordOTPHTMXView.as_view(),
        name='confirm-reset-password-otp-htmx'
    ),
    path(
        'confirm-reset-password-htmx/',
        users_htmx_views.ConfirmResetPasswordHTMXView.as_view(),
        name='confirm-reset-password-htmx'
    ),
    path(
        'unread-notifications-htmx/',
        users_htmx_views.UnreadNotificationsHTMXView.as_view(),
        name='unread-notifications-htmx'
    ),
    path(
        'unread-notifications-icon-htmx/',
        users_htmx_views.UnreadNotificationsIconHTMXView.as_view(),
        name='unread-notifications-icon-htmx'
    ),
    path(
        'change-password-profile-htmx/',
        users_htmx_views.ChangePasswordHTMXView.as_view(),
        name='change-password-profile-htmx'
    ),
    path(
        'change-password-done-profile-htmx/',
        users_htmx_views.ChangePasswordDoneHTMXView.as_view(),
        name='change-password-done-profile-htmx'
    )
]
