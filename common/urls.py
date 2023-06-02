from django.urls import path, include


app_name = 'common'

urlpatterns = [
    path('hx/', include('common.htmx.urls')),
]
