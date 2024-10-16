from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views as users_views

app_name = 'users'

urlpatterns = [
    path('hx/', include('users.htmx.urls')),
    path('login/', users_views.ShnLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', users_views.RegisterView.as_view(), name='register'),
    path('send-otp-register/', users_views.SendRegisterOTPView.as_view(), name='send-otp-register'),
    path('confirm-register/', users_views.ConfirmRegisterOTPView.as_view(), name='confirm-register'),
    path('send-otp-login/', users_views.SendLoginOTPView.as_view(), name='send-otp-login'),
    path('confirm-login/', users_views.ConfirmLoginOTPView.as_view(), name='confirm-login'),
    path('reset-password/', users_views.ResetPasswordView.as_view(), name='reset-password'),
    path('send-otp-reset-password/', users_views.SendResetPasswordOTPView.as_view(), name='send-otp-reset-password'),
    path(
        'confirm-reset-password-otp/',
        users_views.ConfirmResetPasswordOTPView.as_view(),
        name='confirm-reset-password-otp'
    ),
    path('confirm-reset-password/', users_views.ConfirmResetPasswordView.as_view(), name='confirm-reset-password'),
]
