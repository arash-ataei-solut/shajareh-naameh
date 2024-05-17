from django.urls import path, include

from persons.views import PersonAddView, FindMyselfView, PersonUpdateView, PersonDetailView, PersonAddMyselfView, \
    PersonDetailMyselfView

app_name = 'persons'

urlpatterns = [
    path('person-add/', PersonAddView.as_view(), name='person-add'),
    path('person-add-myself/', PersonAddMyselfView.as_view(), name='person-add-myself'),
    path('person-update/<int:pk>/', PersonUpdateView.as_view(), name='person-update'),
    path('person-detail/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('person-detail-myself/', PersonDetailMyselfView.as_view(), name='person-detail-myself'),
    path('find-myself/', FindMyselfView.as_view(), name='find-myself'),
]
