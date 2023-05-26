from django.urls import path, include

from common.views import ChatView

app_name = 'common'

urlpatterns = [
    path('hx/', include('common.htmx.urls')),
    path('chat/', ChatView.as_view(), name='chat')
]
