from django.contrib.auth.views import LogoutView
from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    path('hx/', include('users.htmx.urls')),
    path('login/', views.ShnLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('send-otp-register/', views.SendRegisterOTPView.as_view(), name='send-otp-register'),
    path('confirm-register/', views.ConfirmRegisterOTPView.as_view(), name='confirm-register'),
    path('send-otp-login/', views.SendLoginOTPView.as_view(), name='send-otp-login'),
    path('confirm-login/', views.ConfirmLoginOTPView.as_view(), name='confirm-login'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('send-otp-reset-password/', views.SendResetPasswordOTPView.as_view(), name='send-otp-reset-password'),
    path(
        'confirm-reset-password-otp/',
        views.ConfirmResetPasswordOTPView.as_view(),
        name='confirm-reset-password-otp'
    ),
    path('confirm-reset-password/', views.ConfirmResetPasswordView.as_view(), name='confirm-reset-password'),
    path('personal-info-profile/', views.PersonalInfoProfileView.as_view(), name='personal-info-profile'),
    path(
        'notifications-list-profile/',
        views.NotificationsListProfileView.as_view(),
        name='notifications-list-profile'
     ),
    path('change-password-profile/', views.ChangePasswordView.as_view(), name='change-password-profile'),
    path(
        'change-password-done-profile/',
        views.ChangePasswordDoneView.as_view(),
        name='change-password-done-profile'
    ),
    path(
        'person-list/',
        views.PersonListView.as_view(),
        name='person-list'
    ),
    path(
        'relation-matching-request-list/',
        views.RelationMatchingRequestListView.as_view(),
        name='relation-matching-request-list'
    ),
    path(
        'my-relation-matching-request-list/',
        views.MyRelationMatchingRequestListView.as_view(),
        name='my-relation-matching-request-list'
    )
]
