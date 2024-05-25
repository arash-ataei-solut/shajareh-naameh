from django.urls import path, include

from persons import views
from persons.views import PersonAddView, FindMyselfView, PersonUpdateView, PersonDetailView, PersonAddMyselfView, \
    PersonDetailMyselfView

app_name = 'persons'

urlpatterns = [
    path('person-add/', PersonAddView.as_view(), name='person-add'),
    path('person-add-myself/', PersonAddMyselfView.as_view(), name='person-add-myself'),
    path('person-add-father/<int:person_id>/', views.PersonAddFatherView.as_view(), name='person-add-father'),
    path('person-add-father-myself/', views.PersonAddFatherMyselfView.as_view(), name='person-add-father-myself'),
    path('person-add-mother/<int:person_id>/', views.PersonAddMotherView.as_view(), name='person-add-mother'),
    path('person-add-mother-myself/', views.PersonAddMotherMyselfView.as_view(), name='person-add-mother-myself'),
    path('person-add-spouse/<int:person_id>/', views.PersonAddSpouseView.as_view(), name='person-add-spouse'),
    path('person-add-spouse-myself/', views.PersonAddSpouseMyselfView.as_view(), name='person-add-spouse-myself'),
    path('person-add-child/<int:person_id>/', views.PersonAddChildView.as_view(), name='person-add-child'),
    path('person-add-child-myself/', views.PersonAddChildMyselfView.as_view(), name='person-add-child-myself'),
    path('person-update/<int:pk>/', PersonUpdateView.as_view(), name='person-update'),
    path('person-detail/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('person-detail-myself/', PersonDetailMyselfView.as_view(), name='person-detail-myself'),
    path('find-myself/', FindMyselfView.as_view(), name='find-myself'),
]
