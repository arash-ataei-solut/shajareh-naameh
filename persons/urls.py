from django.urls import path

from persons import views
from persons.views import PersonAddView, FindMyselfView, PersonUpdateView, PersonDetailView, PersonAddMyselfView

app_name = 'persons'

urlpatterns = [
    path('person-add/', PersonAddView.as_view(), name='person-add'),
    path('person-add-myself/', PersonAddMyselfView.as_view(), name='person-add-myself'),

    path('person-add-father/<int:person_pk>/', views.PersonAddFatherView.as_view(), name='person-add-father'),

    path('person-add-mother/<int:person_pk>/', views.PersonAddMotherView.as_view(), name='person-add-mother'),

    path('person-add-spouse/<int:person_pk>/', views.PersonAddSpouseView.as_view(), name='person-add-spouse'),

    path('person-add-child/<int:person_pk>/', views.PersonAddChildView.as_view(), name='person-add-child'),

    path('person-update/<int:pk>/', PersonUpdateView.as_view(), name='person-update'),
    path('person-detail/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('find-myself/', FindMyselfView.as_view(), name='find-myself'),
]
