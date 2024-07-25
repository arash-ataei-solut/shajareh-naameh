from django.urls import path

from persons import views

app_name = 'persons'

urlpatterns = [
    path('person-add/', views.PersonAddView.as_view(), name='person-add'),
    path('person-add-myself/', views.PersonAddMyselfView.as_view(), name='person-add-myself'),

    # Person add relatives
    path('person-add-father/<int:person_pk>/', views.PersonAddFatherView.as_view(), name='person-add-father'),
    path('person-add-mother/<int:person_pk>/', views.PersonAddMotherView.as_view(), name='person-add-mother'),
    path('person-add-spouse/<int:person_pk>/', views.PersonAddSpouseView.as_view(), name='person-add-spouse'),
    path('person-add-child/<int:person_pk>/', views.PersonAddChildView.as_view(), name='person-add-child'),

    # Person delete relatives
    path(
        'person-delete-ancestors/<int:ancestor_pk>/',
        views.PersonDeleteAncestorsView.as_view(),
        name='person-delete-ancestors'
    ),
    path(
        'person-delete-ancestors-failure/<int:ancestor_pk>/',
        views.PersonDeleteAncestorsFailureView.as_view(),
        name='person-delete-ancestors-failure'
    ),

    path('person-update/<int:pk>/', views.PersonUpdateView.as_view(), name='person-update'),
    path('person-detail/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),

    path('person-tree/<int:pk>/', views.PersonTreeView.as_view(), name='person-tree'),

    path(
        'relation-request-select-similar/<int:pk>/',
        views.RelationRequestSelectSimilarView.as_view(),
        name='relation-request-select-similar'
    ),

    path(
        'see-tree-permission-request-create/<int:person_pk>/',
        views.SeeTreePermissionRequestCreateView.as_view(),
        name='see-tree-permission-request-create'
    ),
    path(
        'see-tree-permission-request-success/',
        views.SeeTreePermissionRequestSuccessView.as_view(),
        name='see-tree-permission-request-success'
    ),

    path(
        'person-actions-in-tree/<int:pk>/',
        views.PersonActionsInTreeView.as_view(),
        name='person-actions-in-tree'
    ),

    path('find-myself/', views.FindMyselfView.as_view(), name='find-myself'),
]
