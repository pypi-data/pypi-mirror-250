from django.urls import include, path
from .models import CounterpartyRole, Counterparty, CounterpartyGroup, CounterpartyAssignment
from . import views
from netbox.views.generic import ObjectChangeLogView
from utilities.urls import get_model_urls

urlpatterns = (
    # Contact groups
    path('counterparty-groups/', views.CounterpartyGroupListView.as_view(), name='counterpartygroup_list'),
    path('counterparty-groups/add/', views.CounterpartyGroupEditView.as_view(), name='counterpartygroup_add'),
    path('counterparty-groups/import/', views.CounterpartyGroupBulkImportView.as_view(), name='counterpartygroup_import'),
    path('counterparty-groups/edit/', views.CounterpartyGroupBulkEditView.as_view(), name='counterpartygroup_bulk_edit'),
    path('counterparty-groups/delete/', views.CounterpartyGroupBulkDeleteView.as_view(), name='counterpartygroup_bulk_delete'),
    path('counterparty-groups/<int:pk>/', include(get_model_urls('netbox_counterparties', 'counterpartygroup'))),
    path('counterparty-groups/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='counterpartygroup_changelog', kwargs={
        'model': CounterpartyGroup
    }),

    # counterparty roles
    path('counterparty-roles/', views.CounterpartyRoleListView.as_view(), name='counterpartyrole_list'),
    path('counterparty-roles/add/', views.CounterpartyRoleEditView.as_view(), name='counterpartyrole_add'),
    path('counterparty-roles/import/', views.CounterpartyRoleBulkImportView.as_view(), name='counterpartyrole_import'),
    path('counterparty-roles/edit/', views.CounterpartyRoleBulkEditView.as_view(), name='counterpartyrole_bulk_edit'),
    path('counterparty-roles/delete/', views.CounterpartyRoleBulkDeleteView.as_view(), name='counterpartyrole_bulk_delete'),
    path('counterparty-roles/<int:pk>/', include(get_model_urls('netbox_counterparties', 'counterpartyrole'))),
    path('counterparty-roles/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='counterpartyrole_changelog', kwargs={
        'model': CounterpartyRole
    }),

    # counterparties
    path('counterparties/', views.CounterpartyListView.as_view(), name='counterparty_list'),
    path('counterparties/add/', views.CounterpartyEditView.as_view(), name='counterparty_add'),
    path('counterparties/import/', views.CounterpartyBulkImportView.as_view(), name='counterparty_import'),
    path('counterparties/edit/', views.CounterpartyBulkEditView.as_view(), name='counterparty_bulk_edit'),
    path('counterparties/delete/', views.CounterpartyBulkDeleteView.as_view(), name='counterparty_bulk_delete'),
    path('counterparties/<int:pk>/', include(get_model_urls('netbox_counterparties', 'counterparty'))),
    path('counterparties/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='counterparty_changelog',
         kwargs={
             'model': Counterparty
         }),

    # counterparty assignments
    path('counterparty-assignments/', views.CounterpartyAssignmentListView.as_view(), name='counterpartyassignment_list'),
    path('counterparty-assignments/add/', views.CounterpartyAssignmentEditView.as_view(), name='counterpartyassignment_add'),
    path('counterparty-assignments/import/', views.CounterpartyAssignmentBulkImportView.as_view(), name='counterpartyassignment_import'),
    path('counterparty-assignments/edit/', views.CounterpartyAssignmentBulkEditView.as_view(), name='counterpartyassignment_bulk_edit'),
    path('counterparty-assignments/delete/', views.CounterpartyAssignmentBulkDeleteView.as_view(), name='counterpartyassignment_bulk_delete'),
    path('counterparty-assignments/<int:pk>/', include(get_model_urls('netbox_counterparties', 'counterpartyassignment'))),
    path('counterparty-assignments/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='counterpartyassignment_changelog',
         kwargs={
             'model': CounterpartyAssignment
        }),
)
