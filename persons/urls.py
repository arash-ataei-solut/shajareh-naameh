from django.urls import path, include

from persons.views import AddPersonView, FindMyselfView

app_name = 'persons'

urlpatterns = [
    path('add-person/', AddPersonView.as_view(), name='add-person'),
    path('find-myself/', FindMyselfView.as_view(), name='find-myself')
]
