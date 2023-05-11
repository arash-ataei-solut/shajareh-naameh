from django.urls import path

from persons.views import AddPersonView

app_name = 'persons'

urlpatterns = [
    path('add-person/', AddPersonView.as_view(), name='add-person')
]
