from django.urls import path

from common.htmx.views import AnonymousTicketFormView

app_name = 'common-hx'

urlpatterns = [
    path('anonymous-ticket/', AnonymousTicketFormView.as_view(), name='anonymous-ticket')
]
