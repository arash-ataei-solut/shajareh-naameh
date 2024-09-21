from django.urls import path

from persons import views

app_name = 'persons'

urlpatterns = [
    path('person-add/', views.PersonAddView.as_view(), name='person-add'),
    path('person-add-myself/', views.PersonAddMyselfViewMixin.as_view(), name='person-add-myself'),

    # Person add relatives
    path('person-add-father/<int:person_pk>/', views.PersonAddFatherViewMixin.as_view(), name='person-add-father'),
    path('person-add-mother/<int:person_pk>/', views.PersonAddMotherViewMixin.as_view(), name='person-add-mother'),
    path('person-add-spouse/<int:person_pk>/', views.PersonAddSpouseViewMixin.as_view(), name='person-add-spouse'),
    path('person-add-child/<int:person_pk>/', views.PersonAddChildViewMixin.as_view(), name='person-add-child'),

    # Residence place
    path(
        'person-add-residence-place/<int:person_pk>/',
        views.PersonAddResidencePlaceView.as_view(),
        name='person-add-residence-place'
    ),
    path(
        'person-update-residence-place/<int:pk>/',
        views.PersonUpdateResidencePlaceView.as_view(),
        name='person-update-residence-place'
    ),
    path(
        'person-delete-residence-place-confirmation/<int:pk>/',
        views.PersonDeleteResidencePlaceConfirmationView.as_view(),
        name='person-delete-residence-place-confirmation'
    ),
    path(
        'person-delete-residence-place/<int:pk>/',
        views.PersonDeleteResidencePlaceView.as_view(),
        name='person-delete-residence-place'
    ),

    # Person delete relative
    path(
        'person-delete-ancestor-confirmation/<int:pk>/',
        views.PersonDeleteAncestorConfirmationView.as_view(),
        name='person-delete-ancestor-confirmation'
    ),
    path(
        'person-delete-ancestor/<int:pk>/',
        views.PersonDeleteAncestorView.as_view(),
        name='person-delete-ancestor'
    ),
    path(
        'person-delete-ancestor-failure/<int:pk>/',
        views.PersonDeleteAncestorFailureView.as_view(),
        name='person-delete-ancestor-failure'
    ),
    path(
        'person-delete-descendant-confirmation/<int:pk>/',
        views.PersonDeleteDescendantConfirmationView.as_view(),
        name='person-delete-descendant-confirmation'
    ),
    path(
        'person-delete-descendant/<int:pk>/',
        views.PersonDeleteDescendantView.as_view(),
        name='person-delete-descendant'
    ),
    path(
        'person-delete-descendant-failure/<int:pk>/',
        views.PersonDeleteDescendantFailureView.as_view(),
        name='person-delete-descendant-failure'
    ),
    path(
        'person-delete-spouse-confirmation/<int:pk>/',
        views.PersonDeleteSpouseConfirmationView.as_view(),
        name='person-delete-spouse-confirmation'
    ),
    path(
        'person-delete-spouse/<int:pk>/',
        views.PersonDeleteSpouseView.as_view(),
        name='person-delete-spouse'
    ),
    path(
        'person-delete-spouse-failure/<int:pk>/',
        views.PersonDeleteSpouseFailureView.as_view(),
        name='person-delete-spouse-failure'
    ),
    
    # Person delete
    path(
        'person-delete-confirmation/<int:pk>/',
        views.PersonDeleteConfirmationView.as_view(),
        name='person-delete-confirmation'
    ),
    path(
        'person-delete/<int:pk>/',
        views.PersonDeleteView.as_view(),
        name='person-delete'
    ),
    path(
        'person-delete-failure/<int:pk>/',
        views.PersonDeleteFailureView.as_view(),
        name='person-delete-failure'
    ),

    path('person-update/<int:pk>/', views.PersonUpdateView.as_view(), name='person-update'),
    path('person-detail/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),

    # Relation matching request
    path(
        'relation-matching-request-select-similar/<int:pk>/',
        views.RelationMatchingRequestSelectSimilarView.as_view(),
        name='relation-matching-request-select-similar'
    ),
    path(
        'relation-matching-request-remove-similar/<int:pk>/',
        views.RelationMatchingRequestRemoveSimilarView.as_view(),
        name='relation-matching-request-remove-similar'
    ),
    path(
        'relation-matching-request-confirmation/<int:pk>/',
        views.RelationMatchingRequestConfirmationView.as_view(),
        name='relation-matching-request-confirmation'
    ),

    # Tree
    path('person-tree/<int:pk>/', views.PersonTreeView.as_view(), name='person-tree'),
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
