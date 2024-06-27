from django.urls import path

from persons import views

app_name = 'persons'

urlpatterns = [
    path('person-add/', views.PersonAddView.as_view(), name='person-add'),
    path('person-add-myself/', views.PersonAddMyselfView.as_view(), name='person-add-myself'),

    path('person-add-father/<int:person_pk>/', views.PersonAddFatherView.as_view(), name='person-add-father'),

    path('person-add-mother/<int:person_pk>/', views.PersonAddMotherView.as_view(), name='person-add-mother'),

    path('person-add-spouse/<int:person_pk>/', views.PersonAddSpouseView.as_view(), name='person-add-spouse'),

    path('person-add-child/<int:person_pk>/', views.PersonAddChildView.as_view(), name='person-add-child'),

    path('person-update/<int:pk>/', views.PersonUpdateView.as_view(), name='person-update'),
    path('person-detail/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),

    path('person-tree/<int:pk>/', views.PersonTreeView.as_view(), name='person-tree'),

    path(
        'relation-request-select-similar/<int:pk>/',
        views.RelationRequestSelectSimilarView.as_view(),
        name='relation-request-select-similar'
    ),

    path('find-myself/', views.FindMyselfView.as_view(), name='find-myself'),
]
