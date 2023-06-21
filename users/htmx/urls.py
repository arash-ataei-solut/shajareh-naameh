from django.urls import path

from . import views as users_htmx_views

app_name = 'users-hx'

urlpatterns = [
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
]
